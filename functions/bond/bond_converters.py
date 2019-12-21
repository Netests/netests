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
    pass

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

