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
ERROR_HEADER = "Error import [vrf_compare.py]"
HEADER_GET = "[netests - compare_vrf]"

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
    from protocols.vrf import VRF, ListVRF
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bgp")
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

########################################################################################################################
#
# Functions
#
def compare_vrf(nr, vrf_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_vrf,
        vrf_data=vrf_data,
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
def _compare_vrf(task, vrf_data:json):

    verity_vrf = ListVRF(list())

    if VRF_DATA_KEY in task.host.keys():
        for vrf in vrf_data.get(task.host.name, NOT_SET):

            vrf_obj = VRF(
                vrf_name=vrf.get('vrf_name', NOT_SET),
                vrf_id=vrf.get('vrf_id', NOT_SET),
                l3_vni=vrf.get('l3_vni', NOT_SET),
                rd=vrf.get('rd', NOT_SET),
                rt_imp=vrf.get('rt_imp', NOT_SET),
                rt_exp=vrf.get('rt_exp', NOT_SET),

            )

            verity_vrf.vrf_lst.append(vrf_obj)

        is_same = verity_vrf == task.host[VRF_DATA_KEY]

        task.host[VRF_WORKS_KEY] = is_same
        return is_same

    else:
        print(f"Key {VRF_DATA_KEY} is missing for {task.host.name}")
        return False
