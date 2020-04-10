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

ERROR_HEADER = "Error import [bond_gets.py]"
HEADER_GET = "[netests - get_bond]"

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
    from protocols.bond import BOND, ListBOND
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bond")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.bond.bond_converters import _napalm_bond_converter
    from functions.bond.bond_converters import _cumulus_bond_converter
    from functions.bond.bond_converters import _arista_bond_converter
    from functions.bond.bond_converters import _ios_bond_converter
    from functions.bond.bond_converters import _nexus_bond_converter
    from functions.bond.bond_converters import _extreme_vsp_bond_converter
    from functions.bond.bond_converters import _juniper_bond_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bond.bond_converters")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from nornir.core import Nornir
    # To use advanced filters
    from nornir.core.filter import F
    # To execute netmiko commands
    from nornir.plugins.tasks.networking import netmiko_send_command
    # To execute napalm get config
    from nornir.plugins.tasks.networking import napalm_get
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def get_bond(nr: Nornir, filters={}, level=None, own_vars={}):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_bond_get,
        filters=filters,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_bond_get(task, filters:dict):


    if BOND_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or JUNOS_PLATEFORM_NAME in task.host.platform or \
                ARISTA_PLATEFORM_NAME in task.host.platform or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or \
                CISCO_IOS_PLATEFORM_NAME in task.host.platform:
            if 'connexion' in task.host.keys():
                if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_bond(task, filters)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_bond(task, filters)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_bond(task, filters)

            if use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
                _ios_get_bond(task, filters)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_bond(task, filters)

            elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
                _juniper_get_bond(task, filters)

            else:
                _generic_bond_napalm(task, filters)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Bond Name liste
#
def _create_bond_name_list(bond_lst:ListBOND) -> list:
    """
    This function will retrieve all Bond defined in a ListBOND object and return a list with all bond name

    :param bond_lst:
    :return list:
    """
    bond_name_lst = list()

    for bond in bond_lst.bonds_lst:
        bond_name_lst.append(bond.bond_name)

    return bond_name_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_bond_napalm(task, filters):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_bond(task, filters:dict):

    output = task.run(
        name=f"{CUMULUS_GET_BOND}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BOND
    )
    # print(output.result)

    bonds = _cumulus_bond_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result),
        filters=filters
    )

    task.host[BOND_DATA_HOST_KEY] = bonds
    task.host[BOND_DATA_LIST_KEY] = _create_bond_name_list(bonds)

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_bond(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_bond(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_bond(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_bond(task, filters:dict):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _juniper_get_bond(task, filters:dict):
    pass
