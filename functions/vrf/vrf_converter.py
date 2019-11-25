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
ERROR_HEADER = "Error import [vrf_converters.py]"
HEADER_GET = "[netests - vrf_converters]"

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
    from protocols.vrf import VRF, ListVRF
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vrf")
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
# Function for devices which are compatible with NAPALM
#
def _napalm_vrf_converter(hostname:str(), cmd_output:json) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('get_network_instances'):

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf,
                vrf_type=cmd_output.get('get_network_instances').get(vrf).get('type', NOT_SET),
                rd=cmd_output.get('get_network_instances').get(vrf).get('state').get(
                    'route_distinguisher') if cmd_output.get('get_network_instances').get(vrf).get('state').get(
                    'route_distinguisher', NOT_SET) != "" else NOT_SET
            )
        )

    return vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus VRF converter
#
def _cumulus_vrf_converter(hostname:str(), cmd_outputs:list) -> ListVRF:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus VRF converter
#
def _nexus_vrf_converter(hostname:str(), cmd_output:json) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf'):

        vrf_obj = VRF(
            vrf_name=vrf.get('vrf_name', NOT_SET),
            vrf_id=vrf.get('vrf_id', NOT_SET),
        )

        vrf_list.vrf_lst.append(vrf_obj)

    return vrf_list


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista VRF converter
#
def _arista_vrf_converter(hostname:str(), cmd_output:json) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf_name, facts in cmd_output.get('vrfs').items():

        vrf_obj = VRF(
            vrf_name=vrf_name,
            rd=facts.get('routeDistinguisher', NOT_SET)
        )

        vrf_list.vrf_lst.append(vrf_obj)

    return vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper VRF converter
#
def _juniper_vrf_converter(hostname:str(), cmd_output:json) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('instance-information')[0].get('instance-core'):

        if _juniper_vrf_filter(vrf.get('instance-name')[0].get('data', NOT_SET)):
            vrf_obj = VRF()

            vrf_obj.vrf_name = _juniper_vrf_default_mapping(
                vrf.get('instance-name')[0].get('data', NOT_SET)
            )
            vrf_obj.vrf_id = vrf.get('router-id')[0].get('data', NOT_SET)
            vrf_obj.vrf_type = vrf.get('instance-type')[0].get('data', NOT_SET)
            vrf_obj.l3_vni = NOT_SET

            if "instance-vrf" in vrf.keys():
                vrf_obj.rd = vrf.get('instance-vrf')[0].get('route-distinguisher')[0].get('data', NOT_SET)
                vrf_obj.rt_imp = vrf.get('instance-vrf')[0].get('vrf-import')[0].get('data', NOT_SET)
                vrf_obj.rt_exp = vrf.get('instance-vrf')[0].get('vrf-export')[0].get('data', NOT_SET)
                vrf_obj.exp_targ = vrf.get('instance-vrf')[0].get('vrf-import-target')[0].get('data', NOT_SET)
                vrf_obj.exp_targ = vrf.get('instance-vrf')[0].get('vrf-export-target')[0].get('data', NOT_SET)

            vrf_list.vrf_lst.append(vrf_obj)

    return vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper VRF filter
#
def _juniper_vrf_filter(vrf_name:str) -> bool:
    """
    This function will remove Juniper system. VRF
    - "master"
    - "__juniper_private1__"
    - "__juniper_private2__"
    - "__juniper_private4__"
    - "__master.anon__"

    :param vrf_name:
    :return bool: True if the VRF must be added in the list
    """

    return "__" not in vrf_name

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper VRF mapping
#
def _juniper_vrf_default_mapping(vrf_name:str) -> str:
    """
    This function will convert Juniper global/default/master routing instance
    => master => default

    :param vrf_name:
    :return str: "default" is vrf_name = "master" else vrf_name
    """

    if vrf_name == "master":
        return "default"
    else:
        return vrf_name



