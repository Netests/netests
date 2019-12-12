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
ERROR_HEADER = "Error import [mlag_converters.py]"
HEADER_GET = "[netests - mlag_converters]"

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
    from protocols.mlag import MLAG
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mlag")
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
# NAPALM MLAG converter
#
def _napalm_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus MLAG converter
#
def _cumulus_mlag_converter(hostname:str(), cmd_output:json) -> MLAG:

    if cmd_output is None:
        return None

    if "status" in cmd_output.keys():

        return MLAG(
            hostname=hostname,
            local_id=cmd_output.get("status").get("ourId", NOT_SET),
            peer_id=cmd_output.get("status").get("peerId", NOT_SET),
            peer_alive=cmd_output.get("status").get("peerAlive", NOT_SET),
            peer_int=cmd_output.get("status").get("peerIf", NOT_SET),
            peer_ip=cmd_output.get("status").get("peerIp", NOT_SET),
            sys_mac=cmd_output.get("status").get("sysMac", NOT_SET),
            local_role=cmd_output.get("status").get("ourRole", NOT_SET),
            peer_role=cmd_output.get("status").get("peerRole", NOT_SET),
            local_priority=cmd_output.get("status").get("ourPriority", NOT_SET),
            peer_priority=cmd_output.get("status").get("peerPriority", NOT_SET),
            vxlan_anycast_ip=cmd_output.get("status").get("vxlanAnycast", NOT_SET),
        )

    else:
        return MLAG()

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme VSP MLAG converter
#
def _extreme_vsp_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS MLAG converter
#
def _ios_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus MLAG converter
#
def _nexus_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista MLAG converter
#
def _arista_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper MLAG converter
#
def _juniper_mlag_converter(hostname:str(), cmd_output:json) -> None:
    pass

