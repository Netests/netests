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
ERROR_HEADER = "Error import [lldp_gets.py]"
HEADER_GET = "[netests - get_lldp]"
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
    from functions.discovery_protocols.lldp.lldp_converters import _cumulus_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _nexus_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _arista_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _ios_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _extreme_vsp_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _juniper_lldp_converter
    from functions.discovery_protocols.lldp.lldp_converters import _napalm_lldp_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.lldp")
    print(importError)
    exit(EXIT_FAILURE)

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
    print(f"{ERROR_HEADER} texfsm")
    exit(EXIT_FAILURE)
    print(importError)


########################################################################################################################
#
# Functions
#
def get_lldp(nr: Nornir, filters={}, level=None, vars={}):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_lldp_get,
        on_failed=True,
        num_workers=1
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_lldp_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or CISCO_IOS_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_lldp(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_lldp(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_lldp(task)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_lldp(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_lldp(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_lldp(task)

        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_lldp(task)

        else:
            _generic_lldp_napalm(task)

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")


# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_lldp_napalm(task):

    print(f"Start _generic_lldp_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_lldp_neighbors_detail {task.host.platform}",
        task=napalm_get,
        getters=["get_lldp_neighbors_detail"]
    )
    # print(output.result)

    if output.result != "":
        bgp_sessions = _napalm_lldp_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )

        task.host[LLDP_DATA_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_lldp(task):

    output = task.run(
            name=f"{CUMULUS_GET_LLDP_CDP}",
            task=netmiko_send_command,
            command_string=CUMULUS_GET_LLDP_CDP
    )
    #print_result(output)

    lldp_sessions = _cumulus_lldp_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus (NXOS)
#
def _nexus_get_lldp(task):

    output = task.run(
            name=f"{NEXUS_GET_LLDP}",
            task=netmiko_send_command,
            command_string=NEXUS_GET_LLDP
    )
    #print_result(output)

    lldp_sessions = _nexus_lldp_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_lldp(task):

    output = task.run(
            name=f"{ARISTA_GET_LLDP}",
            task=netmiko_send_command,
            command_string=ARISTA_GET_LLDP
    )
    #print_result(output)

    lldp_sessions = _arista_lldp_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_lldp(task):

    output = task.run(
            name=f"{IOS_GET_LLDP}",
            task=netmiko_send_command,
            command_string=IOS_GET_LLDP
    )
    #print_result(output)


    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_lldp_neighbors_detail.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example =[
        # ['Gi0/3', '001e.7a1f.a100', 'Gi5', 'GigabitEthernet5', 'spine03.dh.local',
        # 'Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)',
        # 'R', '10.0.5.103', '']]
        # type = list() of list()

    lldp_sessions = _ios_lldp_converter(
        hostname=task.host.name,
        cmd_output=parsed_results
    )

    task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_lldp(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks Junos
#
def _juniper_get_lldp(task):

    output = task.run(
        name=f"{JUNOS_GET_LLDP}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_LLDP,
        enable=True
    )
    #print_result(output)

    lldp_sessions = _juniper_lldp_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP
#
def _extreme_vsp_get_lldp(task):

    output = task.run(
        name=f"{EXTREME_VSP_GET_LLDP}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_LLDP,
        enable=True
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_lldp_neighbor.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example =[
        # ['1/1', '50:00:00:03:00:00:', 'swp2', 'leaf01', 'Br', '',
        # 'Cumulus Linux version 3.7.9 running on Bochs Bochs', '10.255.255.201']]
        # type = list() of list()

        lldp_sessions = _extreme_vsp_lldp_converter(
            hostname=task.host.name,
            cmd_output=parsed_results
        )

        task.host[LLDP_DATA_HOST_KEY] = lldp_sessions

