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
ERROR_HEADER = "Error import [bond_converters.py]"
HEADER_GET = "[netests - bond_converters]"

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
    from protocols.bond import BOND, ListBOND
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bond")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
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
# NAPALM bond converter
#
def _napalm_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus bond converter
#
def _cumulus_bond_converter(hostname:str(), cmd_output:json, filters:dict) -> ListBOND:

    if cmd_output is None:
        return None

    bonds_lst = ListBOND(
        bonds_lst=list()
    )

    for bond_name in cmd_output:
        port_lst = list()
        for port in cmd_output.get(bond_name).get("iface_obj").get("members"):
            port_lst.append(
                _mapping_interface_name(
                    port
                )
            )

        bonds_lst.bonds_lst.append(
            BOND(
                bond_name=bond_name,
                ports_members=port_lst,
                vlans_members=_cumulus_retrieve_vlan_per_bond(
                    cmd_output=cmd_output.get(bond_name),
                    filters=filters
                ),
                native_vlan=cmd_output.get(bond_name).get("iface_obj").get("native_vlan"),
                mode=cmd_output.get(bond_name).get("mode", NOT_SET)
            )
        )

    return bonds_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus retrieve VLAN numbers
#
def _cumulus_retrieve_vlan_per_bond(cmd_output:json, filters:dict) -> list:
    """
    This function will retrieve VLAN assigned to a BOND
    "vlan": [
                {
                    "flags": [
                        "PVID",
                        "Egress Untagged"
                    ],
                    "vlan": 1
                },
                {
                    "flags": [],
                    "vlan": 1000,
                    "vlanEnd": 1005
                }
            ],

    :param cmd_output:
    :param filters:
    :return:
    """

    return_lst = list()

    for vlan_block in cmd_output.get("iface_obj").get("vlan"):
        if "vlanEnd" in vlan_block.keys():
            i = 0
            while (vlan_block.get("vlan")+i) <= vlan_block.get("vlanEnd"):
                return_lst.append(str(vlan_block.get("vlan") + i))
                i += 1

        else:
            return_lst.append(str(vlan_block.get("vlan")))

    return return_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme VSP bond converter
#
def _extreme_vsp_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS bond converter
#
def _ios_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus bond converter
#
def _nexus_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista bond converter
#
def _arista_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper bond converter
#
def _juniper_bond_converter(hostname:str(), cmd_output:json) -> ListBOND:
    pass

