#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [static_converters.py]"
HEADER_GET = "[netests - static_converters]"

########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.static import Static, ListStatic
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.static")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks STATIC converter
#
def _cumulus_static_converter(hostname:str(), cmd_outputs:list, vrf_dict:dict()) -> ListStatic:

    static_routes_lst = ListStatic(
        static_routes_lst=list()
    )

    for cmd_output in cmd_outputs:

        if "ipv4 unicast" in cmd_output.keys():

            for prefix in cmd_output.get('ipv4 unicast').keys():

                for facts in cmd_output.get('ipv4 unicast').get(prefix):

                    index_slash = str(facts.get('prefix')).find("/")

                    real_vrf = ""
                    for vrf, vrfid in vrf_dict.items():
                        try:
                            if int(facts.get('vrfId', NOT_SET)) == int(vrfid):
                                real_vrf = vrf
                        except Exception as e:
                            pass

                    static_obj = Static(
                        vrf_name=real_vrf,
                        prefix=str(facts.get('prefix'))[:index_slash],
                        netmask=str(facts.get('prefix'))[index_slash+1:],
                        nexthop=facts.get('nexthops')[0].get('ip', NOT_SET),
                        is_in_fib=facts.get('nexthops')[0].get('fib', NOT_SET),
                        out_interface=facts.get('nexthops')[0].get('interfaceName', NOT_SET),
                        preference=facts.get('distance', NOT_SET),
                        metric=facts.get('metric', NOT_SET)
                    )

                    static_routes_lst.static_routes_lst.append(static_obj)

        else:
            for prefix in cmd_output.keys():

                for facts in cmd_output.get(prefix):
                    index_slash = str(facts.get('prefix')).find("/")

                    static_obj = Static(
                        vrf_name="default",
                        prefix=str(facts.get('prefix'))[:index_slash],
                        netmask=str(facts.get('prefix'))[index_slash+1:],
                        nexthop=facts.get('nexthops')[0].get('ip', NOT_SET),
                        is_in_fib=facts.get('nexthops')[0].get('fib', NOT_SET),
                        out_interface=_mapping_interface_name(facts.get('nexthops')[0].get('interfaceName', NOT_SET)),
                        preference=facts.get('distance', NOT_SET),
                        metric=facts.get('metric', NOT_SET)
                    )

                    static_routes_lst.static_routes_lst.append(static_obj)

    return static_routes_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus STATIC Converter
#
def _nexus_static_converter(hostname:str(), cmd_outputs:list) -> ListStatic:

    static_routes_lst = ListStatic(
        static_routes_lst=list()
    )

    for cmd_output in cmd_outputs:
        if 'TABLE_vrf' in cmd_output.keys():

            if isinstance(cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                    'TABLE_prefix').get('ROW_prefix'), list):

                for facts in cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                        'TABLE_prefix').get('ROW_prefix'):

                    index_slash = str(facts.get('ipprefix')).find("/")

                    static_obj = Static(
                        vrf_name=cmd_output.get('TABLE_vrf').get('ROW_vrf').get('vrf-name-out', NOT_SET),
                        prefix=str(facts.get('ipprefix'))[:index_slash],
                        netmask=str(facts.get('ipprefix'))[index_slash + 1:],
                        nexthop=facts.get('TABLE_path').get('ROW_path').get('ipnexthop', NOT_SET),
                        is_in_fib=facts.get('TABLE_path').get('ROW_path').get('ubest', NOT_SET),
                        out_interface=NOT_SET,
                        preference=facts.get('TABLE_path').get('ROW_path').get('pref', NOT_SET),
                        metric=facts.get('TABLE_path').get('ROW_path').get('metric', NOT_SET)
                    )

                static_routes_lst.static_routes_lst.append(static_obj)

            elif isinstance(cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                    'TABLE_prefix').get('ROW_prefix'), dict):

                for facts in cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                        'TABLE_prefix').values():

                    index_slash = str(facts.get('ipprefix')).find("/")

                    static_obj = Static(
                        vrf_name=cmd_output.get('TABLE_vrf').get('ROW_vrf').get('vrf-name-out', NOT_SET),
                        prefix=str(facts.get('ipprefix'))[:index_slash],
                        netmask=str(facts.get('ipprefix'))[index_slash + 1:],
                        nexthop=facts.get('TABLE_path').get('ROW_path').get('ipnexthop', NOT_SET),
                        is_in_fib=facts.get('TABLE_path').get('ROW_path').get('ubest', NOT_SET),
                        out_interface=NOT_SET,
                        preference=facts.get('TABLE_path').get('ROW_path').get('pref', NOT_SET),
                        metric=facts.get('TABLE_path').get('ROW_path').get('metric', NOT_SET)
                    )

                static_routes_lst.static_routes_lst.append(static_obj)

    return static_routes_lst


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista STATIC Converter
#
def _arista_static_converter(hostname:str(), cmd_outputs:list) -> ListStatic:

    static_routes_lst = ListStatic(
        static_routes_lst=list()
    )

    for cmd_output in cmd_outputs:

        for vrf_name in cmd_output.get('vrfs').keys():

            for prefix, facts in cmd_output.get('vrfs').get(vrf_name).get("routes").items():

                index_slash = str(prefix).find("/")

                static_obj = Static(
                    vrf_name=vrf_name,
                    prefix=str(prefix)[:index_slash],
                    netmask=str(prefix)[index_slash + 1:],
                    nexthop=facts.get('vias')[0].get('nexthopAddr', NOT_SET),
                    is_in_fib=facts.get('kernelProgrammed'),
                    out_interface=_mapping_interface_name(facts.get('vias')[0].get('interface', NOT_SET)),
                    preference=facts.get('preference'),
                    metric=facts.get('metric')
                )

                static_routes_lst.static_routes_lst.append(static_obj)

    return static_routes_lst