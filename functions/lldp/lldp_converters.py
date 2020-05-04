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
    from functions.discovery_protocols.discovery_functions import _mapping_sys_capabilities
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
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

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if "lldp" in cmd_output.keys():
        if "interface" in cmd_output.get('lldp')[0].keys():
            for lldp_neighbor in cmd_output.get('lldp')[0].get("interface"):

                if lldp_neighbor.get("via", NOT_SET) == "LLDP":

                    neighbor_type_lst = list()

                    if lldp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET) == NOT_SET:
                        neighbor_os = NOT_SET
                    else:
                        neighbor_os = lldp_neighbor.get("chassis", NOT_SET)[0].get("descr", NOT_SET)[0].get("value",
                                                                                                            NOT_SET)

                    for capability in lldp_neighbor.get("chassis", NOT_SET)[0].get("capability", NOT_SET):
                        neighbor_type_lst.append(capability.get("type", NOT_SET))

                    lldp_neighbors_lst.lldp_neighbors_lst.append(
                        LLDP(
                            local_name=hostname,
                            local_port=_mapping_interface_name(
                                lldp_neighbor.get("name", NOT_SET)
                            ),
                            neighbor_mgmt_ip=lldp_neighbor.get("chassis", NOT_SET)[0].get("mgmt-ip", NOT_SET)[0].get(
                                "value", NOT_SET),
                            neighbor_name=lldp_neighbor.get("chassis", NOT_SET)[0].get("name", NOT_SET)[0].get("value",
                                                                                                               NOT_SET),
                            neighbor_port=_mapping_interface_name(
                                lldp_neighbor.get("port", NOT_SET)[0].get("id", NOT_SET)[0].get("value", NOT_SET)
                            ),
                            neighbor_os=neighbor_os,
                            neighbor_type=neighbor_type_lst
                        )
                    )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS LLDP converter
#
def _nexus_lldp_converter(hostname:str(), cmd_output:json) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if "TABLE_nbor_detail" in cmd_output.keys():

            for lldp_neighbor in cmd_output.get('TABLE_nbor_detail', NOT_SET).get("ROW_nbor_detail", NOT_SET):

                neighbor_type_lst = list()

                for sys_capability in lldp_neighbor.get("system_capability", NOT_SET):
                    neighbor_type_lst.append(_mapping_sys_capabilities(sys_capability))

                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=_mapping_interface_name(
                            lldp_neighbor.get("l_port_id", NOT_SET)
                        ),
                        neighbor_mgmt_ip=lldp_neighbor.get("mgmt_addr", NOT_SET),
                        neighbor_name=lldp_neighbor.get("sys_name", NOT_SET),
                        neighbor_port=_mapping_interface_name(
                            lldp_neighbor.get("port_id", NOT_SET)
                        ),
                        neighbor_os=lldp_neighbor.get("sys_desc", NOT_SET),
                        neighbor_type=neighbor_type_lst
                    )
                )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS LLDP converter
#
def _arista_lldp_converter(hostname:str(), cmd_output:json) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if "lldpNeighbors" in cmd_output.keys():

        for interface_name, facts in cmd_output.get("lldpNeighbors", NOT_SET).items():
            if len(facts.get("lldpNeighborInfo")) > 0:
                for data in facts.get("lldpNeighborInfo", NOT_SET):

                    neighbor_type_lst = list()
                    for sys_capability in data.get("systemCapabilities", NOT_SET):
                        neighbor_type_lst.append((str(sys_capability).capitalize()))

                    neighbor_mgmt_ip = str()
                    for address in data.get("managementAddresses", NOT_SET):
                        if address.get("addressType", NOT_SET) == "ipv4":
                            neighbor_mgmt_ip = address.get("address", NOT_SET)

                    lldp_neighbors_lst.lldp_neighbors_lst.append(
                        LLDP(
                            local_name=hostname,
                            local_port=_mapping_interface_name(
                                interface_name
                            ),
                            neighbor_mgmt_ip=neighbor_mgmt_ip,
                            neighbor_name=data.get("systemName", NOT_SET),
                            neighbor_port=_mapping_interface_name(
                                data.get("neighborInterfaceInfo", NOT_SET).get("interfaceDescription", NOT_SET)
                            ),
                            neighbor_os=data.get("systemDescription", NOT_SET),
                            neighbor_type=neighbor_type_lst
                        )
                    )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cico IOS LLDP converter
#
def _ios_lldp_converter(hostname:str(), cmd_output:list) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    for lldp_neighbor in cmd_output:

        neighbor_type_lst = list()
        for sys_capability in lldp_neighbor[6]:
            neighbor_type_lst.append(
                _mapping_sys_capabilities(
                    str(sys_capability).capitalize()
                )
            )

        lldp_neighbors_lst.lldp_neighbors_lst.append(

            LLDP(
                local_name=hostname,
                local_port=_mapping_interface_name(
                    lldp_neighbor[0]
                ),
                neighbor_mgmt_ip=lldp_neighbor[7],
                neighbor_name=lldp_neighbor[4],
                neighbor_port=_mapping_interface_name(
                    lldp_neighbor[3]
                ),
                neighbor_os=lldp_neighbor[5],
                neighbor_type=neighbor_type_lst
            )
        )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP LLDP converter
#
def _extreme_vsp_lldp_converter(hostname:str(), cmd_output:list) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    for lldp_neighbor in cmd_output:

        neighbor_type_lst = list()
        for sys_capability in lldp_neighbor[4]:
            neighbor_type_lst.append(
                _mapping_sys_capabilities(
                    str(sys_capability).capitalize()
                )
            )

        lldp_neighbors_lst.lldp_neighbors_lst.append(
            LLDP(
                local_name=hostname,
                local_port=_mapping_interface_name(
                    lldp_neighbor[0]
                ),
                neighbor_mgmt_ip=lldp_neighbor[7],
                neighbor_name=lldp_neighbor[3],
                neighbor_port=_mapping_interface_name(
                    lldp_neighbor[2]
                ),
                neighbor_os=lldp_neighbor[6],
                neighbor_type=neighbor_type_lst
            )
        )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper LLDP converter
#
def _juniper_lldp_converter(hostname:str(), cmd_output:dict) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if "lldp-neighbors-information" in cmd_output.keys():
        if "lldp-neighbor-information" in cmd_output.get("lldp-neighbors-information")[0].keys():
            for neighbors in cmd_output.get("lldp-neighbors-information")[0].get("lldp-neighbor-information"):

                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=_mapping_interface_name(
                            neighbors.get("lldp-local-port-id")[0].get("data")
                        ),
                        neighbor_mgmt_ip=NOT_SET,
                        neighbor_name=neighbors.get("lldp-remote-system-name")[0].get("data"),
                        neighbor_port=_mapping_interface_name(
                            neighbors.get("lldp-remote-port-id")[0].get("data")
                        ),
                        neighbor_os=NOT_SET,
                        neighbor_type=NOT_SET
                    )
                )

    return lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM LLDP converter
#
def _napalm_lldp_converter(hostname:str(), cmd_output:json) -> ListLLDP:

    if cmd_output is None or cmd_output == "":
        return None

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if "get_lldp_neighbors_detail" in cmd_output.keys():
            for interface_name, facts in cmd_output.get("get_lldp_neighbors_detail", NOT_SET).items():

                for neighbors in facts:

                    lldp_neighbors_lst.lldp_neighbors_lst.append(
                        LLDP(
                            local_name=hostname,
                            local_port=_mapping_interface_name(
                                interface_name
                            ),
                            neighbor_mgmt_ip=NOT_SET,
                            neighbor_name=neighbors.get('remote_system_name', NOT_SET),
                            neighbor_port=_mapping_interface_name(
                                neighbors.get('remote_port', NOT_SET)
                            ),
                            neighbor_os=neighbors.get('remote_system_description', NOT_SET),
                            neighbor_type=_mapping_sys_capabilities(
                                neighbors.get('remote_system_capab', NOT_SET)
                            )
                        )
                    )

    return lldp_neighbors_lst
