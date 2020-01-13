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
ERROR_HEADER = "Error import [lldp_compare.py]"
HEADER_GET = "[netests - compare_lldp]"

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

try:
    from protocols.lldp import LLDP, ListLLDP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.lldp")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def compare_lldp(nr, lldp_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_lldp,
        lldp_yaml_data=lldp_yaml_data,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(f"{HEADER_GET} Task '_compare' has failed for {value.host} (value.result={value.result}).")
            return_value = False

    return (not data.failed and return_value)

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare Transit function
#
def _compare_transit_lldp(task, lldp_yaml_data:json):

    task.host[LLDP_WORKS_KEY] = _compare_lldp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        lldp_host_data=task.host[LLDP_DATA_HOST_KEY],
        lldp_yaml_data=lldp_yaml_data,
    )

    return task.host[LLDP_WORKS_KEY]

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_lldp(host_keys, hostname, lldp_host_data, lldp_yaml_data:json):

    verity_lldp = ListLLDP(list())

    if LLDP_DATA_HOST_KEY in host_keys:

        for lldp_neighbor in lldp_yaml_data.get(hostname, NOT_SET):
            lldp_obj = LLDP(
                local_name=hostname,
                local_port=_mapping_interface_name(
                    lldp_neighbor.get("local_port", NOT_SET)
                ),
                neighbor_name=lldp_neighbor.get("neighbor_name", NOT_SET),
                neighbor_port=_mapping_interface_name(
                    lldp_neighbor.get("neighbor_port", NOT_SET)
                )
            )

            verity_lldp.lldp_neighbors_lst.append(lldp_obj)

        return verity_lldp == lldp_host_data

    else:
        print(f"[{HEADER_GET}] {hostname} is not present in {PATH_TO_VERITY_FILES}/{TEST_TO_EXC_LLDP_KEY}.")
        return False
