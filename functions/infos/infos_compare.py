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
ERROR_HEADER = "Error import [infos_compare.py]"
HEADER_GET = "[netests - compare_infos]"

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
    from protocols.infos import SystemInfos
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.infos")
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
def compare_infos(nr, infos_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_infos,
        infos_data=infos_data,
        on_failed=True,
        num_workers=10
    )
    # print_result(data)

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
def _compare_infos(task, infos_data:json):

    verity_infos = SystemInfos()

    if INFOS_DATA_HOST_KEY in task.host.keys():
        if task.host.name in infos_data.keys():
            verity_infos.hostname = task.host.name
            verity_infos.domain = infos_data.get(task.host.name).get('domain', NOT_SET)
            verity_infos.version = infos_data.get(task.host.name).get('version', NOT_SET)
            verity_infos.serial = infos_data.get(task.host.name).get('serial', NOT_SET)
            verity_infos.base_mac = infos_data.get(task.host.name).get('serial', NOT_SET)
            verity_infos.memory = infos_data.get(task.host.name).get('memory', NOT_SET)
            verity_infos.vendor = infos_data.get(task.host.name).get('vendor', NOT_SET)
            verity_infos.model = infos_data.get(task.host.name).get('model', NOT_SET)
            verity_infos.snmp_ips = infos_data.get(task.host.name).get('snmp_ips', list())
            verity_infos.interfaces_lst = infos_data.get(task.host.name).get('interfaces', list())

        is_same = verity_infos == task.host[INFOS_DATA_HOST_KEY]

        task.host[INFOS_WORKS_KEY] = is_same
        return is_same

    else:
        print(f"Key {INFOS_DATA_HOST_KEY} is missing for {task.host.name}")