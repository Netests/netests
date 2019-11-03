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
ERROR_HEADER = "Error import [lldp_converters.py]"
HEADER_GET = "[netests - lldp_converters]"

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
    from protocols.lldp import LLDP, ListLLDP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.lldp")
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
# Cumulus Networks LLDP converter
#
def _cumulus_lldp_converter(hostname:str(), cmd_outputs:json) -> ListLLDP:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS LLDP converter
#
def _nexus_lldp_converter(hostname:str(), cmd_outputs:json) -> ListLLDP:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS LLDP converter
#
def _arista_lldp_converter(hostname:str(), cmd_outputs:json) -> ListLLDP:
    pass
