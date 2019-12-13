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
ERROR_HEADER = "Error import [vlan_compare.py]"
HEADER_GET = "[netests - compare_vlan]"

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
    from protocols.vlan import VLAN, ListVLAN
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vlan")
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
def compare_vlan(nr, vlan_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_vlan,
        vlan_yaml_data=vlan_yaml_data,
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
def _compare_transit_vlan(task, vlan_yaml_data:json):

    task.host[VLAN_WORKS_KEY] = _compare_vlan(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        vlan_host_data=task.host[VLAN_DATA_HOST_KEY],
        vlan_yaml_data=vlan_yaml_data,
    )

    return task.host[VLAN_WORKS_KEY]

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_vlan(host_keys, hostname, vlan_host_data:None, vlan_yaml_data:json) -> bool:

    if vlan_yaml_data is None:
        return False

    if VLAN_DATA_HOST_KEY in host_keys and hostname in vlan_yaml_data.keys():
        pass

    else:
        print(f"[{HEADER_GET}] {hostname} is not present in {PATH_TO_VERITY_FILES}/{TEST_TO_EXC_VLAN_KEY}.")



