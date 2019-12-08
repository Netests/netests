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
ERROR_HEADER = "Error import [mtu_compare.py]"
HEADER_GET = "[netests - compare_mtu]"

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
    from protocols.mtu import InterfaceMTU, ListInterfaceMTU, MTU
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mtu")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    print(importError)
    exit(EXIT_FAILURE)

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

def compare_mtu(nr, mtu_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_transit_compare_mtu,
        mtu_data=mtu_data,
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
# Compare function
#
def _transit_compare_mtu(task, mtu_data:json):

    task.host[MTU_WORKS_HOST_KEY] = _compare_mtu(
        hostname=task.host.name,
        mtu_host_data=task.host[MTU_DATA_HOST_KEY],
        mtu_yaml_data=mtu_data
    )

    return task.host[MTU_WORKS_HOST_KEY]

def _compare_mtu(hostname:str, mtu_host_data:MTU, mtu_yaml_data:dict):

    if mtu_yaml_data is None:
        return False

    return_value = True
    int_error_lst = list()

    if hostname in mtu_yaml_data.keys():

        for interface in mtu_host_data.interface_mtu_lst.interface_mtu_lst:

            if MTU_INTER_YAML_KEY in mtu_yaml_data.get(hostname) and \
                    interface.interface_name in mtu_yaml_data.get(hostname).get(MTU_INTER_YAML_KEY).keys():
                if str(interface.mtu_size) != str(
                        mtu_yaml_data.get(hostname).get(MTU_INTER_YAML_KEY).get(interface.interface_name)):
                    return_value = False
                    int_error_lst.append(interface)

            elif MTU_GLOBAL_YAML_KEY in mtu_yaml_data.get(hostname):
                if str(interface.mtu_size) != str(mtu_yaml_data.get(hostname).get(MTU_GLOBAL_YAML_KEY)):
                    return_value = False
                    int_error_lst.append(interface)

            else:
                return_value = False

        if len(int_error_lst) > 0 and return_value == False:
            print(f"{HEADER_GET} Error with the following interfaces MTU{int_error_lst} !")

        return return_value

    else:
        print(f"{HEADER_GET} Key {INFOS_DATA_HOST_KEY} is missing for {hostname}")
        return False