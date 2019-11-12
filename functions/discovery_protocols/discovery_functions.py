#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [discovery_functions.py]"
HEADER_GET = "[netests - function_discovery]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# LLDP sysem compability converter
#
def _mapping_sys_capabilities(code) -> str():
    """
    This function will return systeme capability name regarding the abreviation given in parameter

    Output extract from Cisco Nexus9000 9000v Chassis NXOS: version 7.0(3)I7(5a)

    Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

    :param codes: str()
    :return str(): that contains system capability name
    """

    if code == "R" or "router":
        return "Router"
    elif code == "B":
        return "Bridge"
    elif code == "T":
        return "Telephone"
    elif code == "C":
        return "DOCSIS Cable Device"
    elif code == "W":
        return "WLAN Access Point"
    elif code == "P":
        return "Repeater"
    elif code == "S":
        return "Station"
    elif code == "O":
        return "Other"
    else:
        return NOT_SET

# ----------------------------------------------------------------------------------------------------------------------
#
# Mapping inter converter
#
def _mapping_interface_name(int_name) -> str():
    """
    This function will receive an interface name in parameter and return the standard interface name.

    For example:
        * (Arista) Ethernet3 => Eth1/3

    :param int_name:
    :return:
    """

    if "Ethernet1/" in int_name:
        number = ""
        slash_index = int_name.find("/")
        for char in int_name[slash_index:]:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    elif "Ethernet" in int_name:
        number = ""
        for char in int_name:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    else:
        return str(int_name).lower()