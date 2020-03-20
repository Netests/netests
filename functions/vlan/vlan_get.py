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

ERROR_HEADER = "Error import [vlan_gets.py]"
HEADER_GET = "[netests - get_vlan]"

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
    from functions.bond.bond_get import get_bond
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bond.bond_get")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.vlan.vlan_converters import _napalm_vlan_converter
    from functions.vlan.vlan_converters import _cumulus_vlan_converter
    from functions.vlan.vlan_converters import _extreme_vsp_vlan_converter
    from functions.vlan.vlan_converters import _ios_vlan_converter
    from functions.vlan.vlan_converters import _nexus_vlan_converter
    from functions.vlan.vlan_converters import _arista_vlan_converter
    from functions.vlan.vlan_converters import _juniper_vlan_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vlan.vlan_converters")
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
def get_vlan(nr: Nornir, filters:dict):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    if filters.get("get_bond", True):
        get_bond(
            nr=nr,
            filters=filters
        )

    data = devices.run(
        task=generic_vlan_get,
        filters=filters,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_vlan_get(task, filters:dict):


    if VLAN_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or JUNOS_PLATEFORM_NAME in task.host.platform or \
                ARISTA_PLATEFORM_NAME in task.host.platform or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or \
                CISCO_IOS_PLATEFORM_NAME in task.host.platform:
            if 'connexion' in task.host.keys():
                if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_vlan(task, filters)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_vlan(task, filters)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_vlan(task, filters)

            if use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
                _ios_get_vlan(task, filters)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_vlan(task, filters)

            elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
                _juniper_get_vlan(task, filters)

            else:
                _generic_vlan_napalm(task, filters)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_vlan_napalm(task, filters):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_vlan(task, filters:dict):

    outputs_dict = dict()

    output = task.run(
        name=f"{CUMULUS_GET_VLAN_VRF}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN_VRF
    )
    # print(output.result)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cumulus_net_show_vrf_list.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['tenant5', ['vlan1005']], ['tenant5', ['vlan1005-v0']], ['tenant5', ['vlan4005']],
        # ['tenant4', ['vlan1004']], ['tenant4', ['vlan1004-v0']], ['tenant4', ['vlan4004']],
        # ['mgmt', []]]
        # type = list() of list()
        outputs_dict[VLAN_VRF_LIST_KEY] = parsed_results

    output = task.run(
        name=f"{CUMULUS_GET_VLAN}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[VLAN_VRF_DETAIL_KEY] = json.loads(output.result)


    output = task.run(
        name=f"{CUMULUS_GET_VLAN_MEM}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN_MEM
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[VLAN_VRF_MEMBERS_KEY] = json.loads(output.result)

    vlans = _cumulus_vlan_converter(
        bond_lst=task.host[BOND_DATA_LIST_KEY],
        cmd_output=outputs_dict,
        filters=filters
    )

    task.host[VLAN_DATA_HOST_KEY] = vlans

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_vlan(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_vlan(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_vlan(task, filters:dict):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_vlan(task, filters:dict):

    outputs_dict = dict()

    output_get = task.run(
        name=f"{ARISTA_GET_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_VLAN
    )
    # print(output.result)

    output_get_ip = task.run(
        name=f"{ARISTA_GET_IP_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_IP_VLAN
    )
    # print(output.result)

    output_get_int = task.run(
        name=f"{ARISTA_GET_INT_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_INT_VLAN
    )
    # print(output.result)

    if output_get.result != "" and output_get_ip.result != "" and output_get_int.result != "" :
        outputs_dict[VLAN_GET_L2] = json.loads(output_get.result)
        outputs_dict[VLAN_GET_L3] = json.loads(output_get_ip.result)
        outputs_dict[VLAN_GET_INT] = json.loads(output_get_int.result)

    vlans = _arista_vlan_converter(
        cmd_output=outputs_dict,
        filters=filters
    )

    task.host[VLAN_DATA_HOST_KEY] = vlans

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _juniper_get_vlan(task, filters:dict):
    pass
