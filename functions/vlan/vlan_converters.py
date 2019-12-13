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
ERROR_HEADER = "Error import [vlan_converters.py]"
HEADER_GET = "[netests - vlan_converters]"

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
    from protocols.vlan import VLAN, ListVLAN
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vlan")
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
# NAPALM vlan converter
#
def _napalm_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus vlan converter
#
def _cumulus_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme VSP vlan converter
#
def _extreme_vsp_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS vlan converter
#
def _ios_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus vlan converter
#
def _nexus_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vlan converter
#
def _arista_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper vlan converter
#
def _juniper_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

