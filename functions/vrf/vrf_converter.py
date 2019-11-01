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

    for vrf in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET):

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

    for vrf_name, facts in cmd_output.get('vrfs', NOT_SET).items():

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



