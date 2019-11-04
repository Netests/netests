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
ERROR_HEADER = "Error import [cdp_converters.py]"
HEADER_GET = "[netests - cdp_converters]"

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
    from functions.discovery_protocols.discovery_functions import _mapping_sys_capabilities
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.lldp.lldp_functions")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.cdp import CDP, ListCDP
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
def _cumulus_cdp_converter(hostname:str(), cmd_output:json) -> ListCDP:

    cdp_neighbors_lst = ListCDP(list())

    if "lldp" in cmd_output.keys():
        if cmd_output.get('lldp', NOT_SET) is NOT_SET:
            return ListCDP(list())

        else:

            for cdp_neighbor in cmd_output.get('lldp', NOT_SET)[0].get("interface", NOT_SET):

                if "CDP" in cdp_neighbor.get("via", NOT_SET):

                    neighbor_type_lst = list()

                    if cdp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET) == NOT_SET:
                        neighbor_os = NOT_SET
                    else:
                        neighbor_os = cdp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET)[0].get("value", NOT_SET)

                    for capability in cdp_neighbor.get("chassis", NOT_SET)[0].get("capability", NOT_SET):
                        neighbor_type_lst.append(capability.get("type", NOT_SET))


                    lldp_obj = CDP(
                        local_name=hostname,
                        local_port=_mapping_interface_name(cdp_neighbor.get("name", NOT_SET)),
                        neighbor_mgmt_ip=cdp_neighbor.get("chassis", NOT_SET)[0].get("mgmt-ip", NOT_SET)[0].get("value", NOT_SET),
                        neighbor_name=cdp_neighbor.get("chassis", NOT_SET)[0].get("name", NOT_SET)[0].get("value", NOT_SET),
                        neighbor_port=_mapping_interface_name(
                            cdp_neighbor.get("port", NOT_SET)[0].get("id", NOT_SET)[0].get("value", NOT_SET)),
                        neighbor_os=neighbor_os,
                        neighbor_type=neighbor_type_lst
                    )

                    cdp_neighbors_lst.cdp_neighbors_lst.append(lldp_obj)

    return cdp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS LLDP converter
#
def _nexus_cdp_converter(hostname:str(), cmd_output:json) -> ListCDP:

    cdp_neighbors_lst = ListCDP(list())

    if "TABLE_cdp_neighbor_detail_info" in cmd_output.keys():

        for cdp_neighbor in cmd_output.get('TABLE_cdp_neighbor_detail_info', NOT_SET).get(
                "ROW_cdp_neighbor_detail_info", NOT_SET):

                neighbor_type_lst = list()

                for sys_capability in cdp_neighbor.get("capability", NOT_SET):
                    neighbor_type_lst.append(_mapping_sys_capabilities(sys_capability))

                lldp_obj = CDP(
                    local_name=hostname,
                    local_port=_mapping_interface_name(cdp_neighbor.get("intf_id", NOT_SET)),
                    neighbor_mgmt_ip=cdp_neighbor.get("v4addr", NOT_SET),
                    neighbor_name=cdp_neighbor.get("device_id", NOT_SET),
                    neighbor_port=_mapping_interface_name(cdp_neighbor.get("port_id", NOT_SET)),
                    neighbor_os=cdp_neighbor.get("version", NOT_SET),
                    neighbor_type=neighbor_type_lst
                )

                cdp_neighbors_lst.cdp_neighbors_lst.append(lldp_obj)

    return cdp_neighbors_lst