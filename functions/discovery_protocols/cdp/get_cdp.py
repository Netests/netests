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
ERROR_HEADER = "Error import [cdp_gets.py]"
HEADER_GET = "[netests - get_cdp]"
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
    from functions.discovery_protocols.cdp.cdp_converters import _cumulus_cdp_converter
    from functions.discovery_protocols.cdp.cdp_converters import _nexus_cdp_converter
    from functions.discovery_protocols.cdp.cdp_converters import _ios_cdp_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.cdp.cdp_converters")
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
    print(f"{ERROR_HEADER} textfsm")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def get_cdp(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_cdp_get,
        on_failed=True,
        num_workers=1
    )
    print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_cdp_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or CISCO_IOS_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_cdp(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :

        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_cdp(task)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_cdp(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_cdp(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_cdp(task)

        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_cdp(task)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_cdp(task):

    output = task.run(
            name=f"{CUMULUS_GET_LLDP_CDP}",
            task=netmiko_send_command,
            command_string=CUMULUS_GET_LLDP_CDP
    )
    #print_result(output)

    cdp_sessions = _cumulus_cdp_converter(task.host.name, json.loads(output.result))

    task.host[CDP_DATA_HOST_KEY] = cdp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus (NXOS)
#
def _nexus_get_cdp(task):

    output = task.run(
            name=f"{NEXUS_GET_CDP}",
            task=netmiko_send_command,
            command_string=NEXUS_GET_CDP
    )
    #print_result(output)

    cdp_sessions = _nexus_cdp_converter(task.host.name, json.loads(output.result))

    task.host[CDP_DATA_HOST_KEY] = cdp_sessions


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_cdp(task):

    output = task.run(
            name=f"{IOS_GET_CDP}",
            task=netmiko_send_command,
            command_string=IOS_GET_CDP
    )
    #print_result(output)


    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_cdp_neighbors_detail.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example =[
        # ['leaf01', '10.255.255.201', 'Linux', 'eth0', 'GigabitEthernet0/0', 'Cumulus Linux version 3.7.9', 'Router ']
        # type = list() of list()
        print(parsed_results)

    cdp_sessions = _ios_cdp_converter(task.host.name, parsed_results)

    task.host[LLDP_DATA_HOST_KEY] = cdp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_cdp(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_cdp(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks Junos
#
def _juniper_get_cdp(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP
#
def _extreme_vsp_get_cdp(task):
    raise NotImplemented
