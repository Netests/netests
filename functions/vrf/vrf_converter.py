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
def _nxos_vrf_converter(hostname:str(), cmd_output:json) -> ListVRF:

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
# Cisco IOSXR VRF converter
#
def _iosxr_vrf_converter(hostname:str(), cmd_output:list) -> ListVRF:
    return _cisco_vrf_converter(
        hostname,
        cmd_output
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSVRF converter
#
def _ios_vrf_converter(hostname:str(), cmd_output:list) -> ListVRF:
    return _cisco_vrf_converter(
        hostname,
        cmd_output
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Generic (IOS + IOSXR) VRF converter
#
def _cisco_vrf_converter(hostname:str(), cmd_output:list) -> ListVRF:

    vrf_list = ListVRF(list())

    vrf_list.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="0",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            exp_targ=NOT_SET,
            imp_targ=NOT_SET
        )
    )

    for vrf in cmd_output:

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf[0],
                vrf_id=vrf[1],
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=vrf[2] if " " not in vrf[2] else NOT_SET,
                rt_imp=NOT_SET,
                rt_exp=NOT_SET,
                exp_targ=NOT_SET,
                imp_targ=NOT_SET
            )
        )

    return vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP VRF converter
#
def _extreme_vsp_vrf_converter(hostname:str(), cmd_output:list) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output:

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf[0],
                vrf_id=vrf[1],
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=NOT_SET,
                rt_imp=NOT_SET,
                rt_exp=NOT_SET,
                exp_targ=NOT_SET,
                imp_targ=NOT_SET
            )
        )
            
    return vrf_list    

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP VRF mapping
#
def _extreme_vsp_vrf_mapping(vrf_name:str) -> str:
    """
    This function will convert Extreme Networks VSP routing instance (GlobalRouter & MgmtRouter)
    => GlobalRouter => default
    => MgmtRouter => mgmt

    :param vrf_name:
    :return str: "default" if vrf_name = "GlobalRouter" // "mgmt" if vrf_name = "MgmtRouter" // else vrf_name
    """

    if vrf_name == "GlobalRouter":
        return "default"
    elif vrf_name == "MgmtRouter":
        return "mgmt"
    else:
        return vrf_name
