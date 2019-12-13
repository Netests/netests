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
ERROR_HEADER = "Error import [l2vni_converters.py]"
HEADER_GET = "[netests - l2vni_converters]"

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
    from protocols.l2vni import L2VNI, ListL2VNI
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.l2vni")
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
# NAPALM L2VNI converter
#
def _napalm_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus L2VNI converter
#
def _cumulus_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme VSP L2VNI converter
#
def _extreme_vsp_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS L2VNI converter
#
def _ios_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus L2VNI converter
#
def _nexus_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista L2VNI converter
#
def _arista_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper L2VNI converter
#
def _juniper_l2vni_converter(hostname:str(), cmd_output:json) -> ListL2VNI:
    pass

