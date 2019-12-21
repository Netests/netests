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
ERROR_HEADER = "Error import [bond_compare.py]"
HEADER_GET = "[netests - compare_bond]"

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
    from protocols.bond import BOND, ListBOND
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bond")
    exit(EXIT_FAILURE)
    print(importError)

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
def compare_bond(nr, bond_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_bond,
        bond_yaml_data=bond_yaml_data,
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
def _compare_transit_bond(task, bond_yaml_data:json):

    task.host[BOND_WORKS_KEY] = _compare_bond(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        bond_host_data=task.host[BOND_DATA_HOST_KEY],
        bond_yaml_data=bond_yaml_data,
    )

    return task.host[BOND_WORKS_KEY]

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_bond(host_keys, hostname, bond_host_data:None, bond_yaml_data:json) -> bool:

    if bond_yaml_data is None:
        return False

    verity_bonds_lst = ListBOND(
        bonds_lst=list()
    )

    if BOND_DATA_HOST_KEY in host_keys and hostname in bond_yaml_data.keys():
        for bond in bond_yaml_data.get(hostname):

            ports_members = list()
            for port in bond.get("ports_members", NOT_SET):
                ports_members.append(
                    _mapping_interface_name(
                        port
                    )
                )

            verity_bonds_lst.bonds_lst.append(
                BOND(
                    bond_name=bond.get("bond_name", NOT_SET),
                    ports_members=ports_members,
                    vlans_members=bond.get("vlans_members", list()),
                    native_vlan=bond.get("native_vlan", NOT_SET),
                    mode=bond.get("mode", NOT_SET),
                )
            )

        return verity_bonds_lst == bond_host_data

    else:
        print(f"{HEADER_GET} {hostname} is not present in {PATH_TO_VERITY_FILES}/{TEST_TO_EXC_BOND_KEY}.")
        return False