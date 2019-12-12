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
ERROR_HEADER = "Error import [mlag_compare.py]"
HEADER_GET = "[netests - compare_mlag]"

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
    from protocols.mlag import MLAG
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mlag")
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
def compare_mlag(nr, mlag_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_mlag,
        mlag_yaml_data=mlag_yaml_data,
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
def _compare_transit_mlag(task, mlag_yaml_data:json):

    task.host[MLAG_WORKS_KEY] = _compare_mlag(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        mlag_host_data=task.host[MLAG_DATA_HOST_KEY],
        mlag_yaml_data=mlag_yaml_data,
    )

    return task.host[MLAG_WORKS_KEY]

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_mlag(host_keys, hostname, mlag_host_data:None, mlag_yaml_data:json) -> bool:

    if mlag_yaml_data is None:
        return False

    if MLAG_DATA_HOST_KEY in host_keys and hostname in mlag_yaml_data.keys():

        verity_mlag =  MLAG(
            hostname=hostname,
            local_id=mlag_yaml_data.get(hostname).get("local_id", NOT_SET),
            peer_id=mlag_yaml_data.get(hostname).get("peer_id", NOT_SET),
            peer_alive=mlag_yaml_data.get(hostname).get("peer_alive", NOT_SET),
            peer_int=mlag_yaml_data.get(hostname).get("peer_int", NOT_SET),
            peer_ip=mlag_yaml_data.get(hostname).get("peer_ip", NOT_SET),
            sys_mac=mlag_yaml_data.get(hostname).get("sys_mac", NOT_SET),
            local_role=mlag_yaml_data.get(hostname).get("local_role", NOT_SET),
            peer_role=mlag_yaml_data.get(hostname).get("peer_role", NOT_SET),
            local_priority=mlag_yaml_data.get(hostname).get("local_priority", NOT_SET),
            peer_priority=mlag_yaml_data.get(hostname).get("peer_priority", NOT_SET),
            vxlan_anycast_ip=mlag_yaml_data.get(hostname).get("vxlan_anycast_ip", NOT_SET),
        )

        return verity_mlag == mlag_host_data

    else:
        print(f"[{HEADER_GET}] {hostname} is not present in {PATH_TO_VERITY_FILES}/{TEST_TO_EXC_MLAG_KEY}.")



