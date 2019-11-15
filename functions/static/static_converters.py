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
    from protocols.static import Nexthop, ListNexthop, Static, ListStatic
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

                nexthops_lst = ListNexthop(
                    nexthops_lst=list()
                )

                index_slash = str(prefix).find("/")

                for facts in cmd_output.get('ipv4 unicast').get(prefix):

                    real_vrf = ""
                    for vrf, vrfid in vrf_dict.items():
                        try:
                            if int(facts.get('vrfId', NOT_SET)) == int(vrfid):
                                real_vrf = vrf
                        except Exception as e:
                            pass

                    for nexthop in facts.get('nexthops'):

                        nexthop_obj = Nexthop(
                            ip_address=nexthop.get('ip', NOT_SET),
                            is_in_fib=nexthop.get('nexthops', False),
                            out_interface=_mapping_interface_name(nexthop.get('interfaceName', NOT_SET)),
                            preference=facts.get('distance', NOT_SET),
                            metric=facts.get('metric', NOT_SET),
                            active=nexthop.get('nexthops', False)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                static_obj = Static(
                    vrf_name=real_vrf,
                    prefix=str(prefix)[:index_slash],
                    netmask=str(prefix)[index_slash+1:],
                    nexthop=nexthops_lst
                )

                static_routes_lst.static_routes_lst.append(static_obj)

        else:
            for prefix in cmd_output.keys():

                nexthops_lst = ListNexthop(
                    nexthops_lst=list()
                )

                index_slash = str(prefix).find("/")

                for facts in cmd_output.get(prefix):

                    index_slash = str(facts.get('prefix')).find("/")

                    for nexthop in facts.get('nexthops'):

                        nexthop_obj = Nexthop(
                            ip_address=nexthop.get('ip', NOT_SET),
                            is_in_fib=nexthop.get('nexthops', False),
                            out_interface=_mapping_interface_name(nexthop.get('interfaceName', NOT_SET)),
                            preference=facts.get('distance', NOT_SET),
                            metric=facts.get('metric', NOT_SET),
                            active=nexthop.get('nexthops', False)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                static_obj = Static(
                    vrf_name="default",
                    prefix=str(prefix)[:index_slash],
                    netmask=str(prefix)[index_slash+1:],
                    nexthop=nexthops_lst
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

                    nexthops_lst = ListNexthop(
                        nexthops_lst=list()
                    )

                    if isinstance(facts.get('TABLE_path').get('ROW_path'), list):
                        for nexthop in facts.get('TABLE_path').get('ROW_path'):

                            nexthop_obj = Nexthop(
                                ip_address=nexthop.get('ipnexthop', NOT_SET),
                                is_in_fib=nexthop.get('always_true_in_nexus', True),
                                out_interface=NOT_SET,
                                preference=nexthop.get('pref', NOT_SET),
                                metric=nexthop.get('metric', NOT_SET),
                                active=nexthop.get('always_true_in_nexus', True),
                            )

                            nexthops_lst.nexthops_lst.append(nexthop_obj)


                    elif isinstance(facts.get('TABLE_path').get('ROW_path'), dict):

                        nexthop_obj = Nexthop(
                            ip_address=facts.get('TABLE_path').get('ROW_path').get('ipnexthop', NOT_SET),
                            is_in_fib=facts.get('TABLE_path').get('ROW_path').get('always_true_in_nexus', True),
                            out_interface=NOT_SET,
                            preference=facts.get('TABLE_path').get('ROW_path').get('pref', NOT_SET),
                            metric=facts.get('TABLE_path').get('ROW_path').get('metric', NOT_SET),
                            active=facts.get('TABLE_path').get('ROW_path').get('always_true_in_nexus', True)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                    index_slash = str(facts.get('ipprefix')).find("/")

                    static_obj = Static(
                        vrf_name=cmd_output.get('TABLE_vrf').get('ROW_vrf').get('vrf-name-out', NOT_SET),
                        prefix=str(facts.get('ipprefix'))[:index_slash],
                        netmask=str(facts.get('ipprefix'))[index_slash + 1:],
                        nexthop=nexthops_lst
                    )

                    static_routes_lst.static_routes_lst.append(static_obj)

            elif isinstance(cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                    'TABLE_prefix').get('ROW_prefix'), dict):

                for facts in cmd_output.get('TABLE_vrf').get('ROW_vrf').get('TABLE_addrf').get('ROW_addrf').get(
                        'TABLE_prefix').values():

                    nexthops_lst = ListNexthop(
                        nexthops_lst=list()
                    )

                    if isinstance(facts.get('TABLE_path').get('ROW_path'), list):
                        for nexthop in facts.get('TABLE_path').get('ROW_path'):

                            nexthop_obj = Nexthop(
                                ip_address=nexthop.get('ipnexthop', NOT_SET),
                                is_in_fib=nexthop.get('always_true_in_nexus', True),
                                out_interface=NOT_SET,
                                preference=nexthop.get('pref', NOT_SET),
                                metric=nexthop.get('metric', NOT_SET),
                                active=nexthop.get('always_true_in_nexus', True),
                            )

                            nexthops_lst.nexthops_lst.append(nexthop_obj)


                    elif isinstance(facts.get('TABLE_path').get('ROW_path'), dict):

                        nexthop_obj = Nexthop(
                            ip_address=facts.get('TABLE_path').get('ROW_path').get('ipnexthop', NOT_SET),
                            is_in_fib=facts.get('TABLE_path').get('ROW_path').get('always_true_in_nexus', True),
                            out_interface=NOT_SET,
                            preference=facts.get('TABLE_path').get('ROW_path').get('pref', NOT_SET),
                            metric=facts.get('TABLE_path').get('ROW_path').get('metric', NOT_SET),
                            active=facts.get('TABLE_path').get('ROW_path').get('always_true_in_nexus', True)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                    index_slash = str(facts.get('ipprefix')).find("/")

                    static_obj = Static(
                        vrf_name=cmd_output.get('TABLE_vrf').get('ROW_vrf').get('vrf-name-out', NOT_SET),
                        prefix=str(facts.get('ipprefix'))[:index_slash],
                        netmask=str(facts.get('ipprefix'))[index_slash + 1:],
                        nexthop=nexthops_lst
                    )

                    static_routes_lst.static_routes_lst.append(static_obj)

    print(static_routes_lst)
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

                nexthops_lst = ListNexthop(
                    nexthops_lst=list()
                )

                for nexthop in facts.get('vias'):

                    nexthop_obj = Nexthop(
                        ip_address=nexthop.get('nexthopAddr', NOT_SET),
                        is_in_fib=nexthop.get('always_true_in_arista', True),
                        out_interface=_mapping_interface_name(nexthop.get('interface', NOT_SET)),
                        preference=facts.get('preference', NOT_SET),
                        metric=facts.get('metric', NOT_SET),
                        active=nexthop.get('always_true_in_arista', True)
                    )

                    nexthops_lst.nexthops_lst.append(nexthop_obj)

                static_obj = Static(
                    vrf_name=vrf_name,
                    prefix=str(prefix)[:index_slash],
                    netmask=str(prefix)[index_slash + 1:],
                    nexthop=nexthops_lst
                )

                static_routes_lst.static_routes_lst.append(static_obj)

    return static_routes_lst