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
def _cumulus_lldp_converter(hostname:str(), cmd_output:json) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(list())

    if "lldp" in cmd_output.keys():
        if cmd_output.get('lldp', NOT_SET) is NOT_SET:
            return ListLLDP(list())

        else:

            for lldp_neighbor in cmd_output.get('lldp', NOT_SET)[0].get("interface", NOT_SET):

                neighbor_type_lst = list()

                if lldp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET) == NOT_SET:
                    neighbor_os = NOT_SET
                else:
                    neighbor_os = lldp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET)[0].get("value", NOT_SET)

                for capability in lldp_neighbor.get("chassis", NOT_SET)[0].get("capability", NOT_SET):
                    neighbor_type_lst.append(capability.get("type", NOT_SET))


                lldp_obj = LLDP(
                    local_name=hostname,
                    local_port=lldp_neighbor.get("name", NOT_SET),
                    neighbor_mgmt_ip=lldp_neighbor.get("chassis", NOT_SET)[0].get("mgmt-ip", NOT_SET)[0].get("value", NOT_SET),
                    neighbor_name=lldp_neighbor.get("chassis", NOT_SET)[0].get("name", NOT_SET)[0].get("value", NOT_SET),
                    neighbor_port=lldp_neighbor.get("port", NOT_SET)[0].get("id", NOT_SET)[0].get("value",NOT_SET),
                    neighbor_os=neighbor_os,
                    neighbor_type=neighbor_type_lst
                )

                lldp_neighbors_lst.lldp_neighbors_lst.append(lldp_obj)

    print(lldp_neighbors_lst)
    return  lldp_neighbors_lst


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
