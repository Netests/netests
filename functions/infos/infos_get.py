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

ERROR_HEADER = "Error import [infos_gets.py]"
HEADER_GET = "[netests - get_infos]"

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
    from functions.infos.infos_converters import _napalm_infos_converter
    from functions.infos.infos_converters import _cumulus_infos_converter
    from functions.infos.infos_converters import _nexus_infos_converter
    from functions.infos.infos_converters import _arista_infos_converter
    from functions.infos.infos_converters import _juniper_infos_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.infos.infos_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def get_infos(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_infos_get,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_infos_get(task):

    if INFOS_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform or CISCO_PLATEFORM_NAME in task.host.platform or \
                CISCO_IOSXR_PLATEFORM_NAME in task.host.platform:
            if 'connexion' in task.host.keys():
                if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET) == "ssh":
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_infos(task)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_infos(task)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_infos(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_infos(task)

            elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
                _juniper_get_infos(task)

            else:
                _generic_infos_napalm(task)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_infos_napalm(task):

    print(f"Start _generic_infos_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM _generic_infos_napalm {task.host.platform}",
        task=napalm_get,
        getters=["facts"]
    )
    # print(output.result)

    if output.result != "":
        system_infos = _napalm_infos_converter(task.host.platform, output.result)

        task.host[INFOS_DATA_HOST_KEY] = system_infos


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_infos(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{CUMULUS_GET_INFOS}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_INFOS
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{CUMULUS_GET_SNMP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_SNMP
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SNMP_DICT_KEY] = (json.loads(output.result))


    output = task.run(
        name=f"{CUMULUS_GET_IPV4}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_IPV4
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_INT_DICT_KEY] = (json.loads(output.result))

    system_infos = _cumulus_infos_converter(outputs_dict)

    task.host[INFOS_DATA_HOST_KEY] = system_infos

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_infos(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_infos(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{NEXUS_GET_INFOS}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_INFOS
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{NEXUS_GET_SNMP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_SNMP
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SNMP_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{NEXUS_GET_INT}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_INT
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_INT_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{NEXUS_GET_DOMAIN}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_DOMAIN
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_DOMAIN_DICT_KEY] = (json.loads(output.result))

    system_infos = _nexus_infos_converter(outputs_dict)

    task.host[INFOS_DATA_HOST_KEY] = system_infos

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _cisco_get_infos(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_infos(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{ARISTA_GET_INFOS}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_INFOS
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{ARISTA_GET_INT}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_INT
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_INT_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{ARISTA_GET_DOMAIN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_DOMAIN
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_DOMAIN_DICT_KEY] = (json.loads(output.result))

    system_infos = _arista_infos_converter(outputs_dict)

    task.host[INFOS_DATA_HOST_KEY] = system_infos
# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _juniper_get_infos(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{JUNOS_GET_INFOS}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_INFOS
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_INT}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_INT
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_INT_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_MEMORY}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_MEMORY
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_MEMORY_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_CONFIG_SYSTEM}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_CONFIG_SYSTEM
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_CONFIG_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_SERIAL}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_SERIAL
    )
    # print(output.result)

    if output.result != "":
        outputs_dict[INFOS_SERIAL_DICT_KEY] = (json.loads(output.result))

    system_infos = _juniper_infos_converter(outputs_dict)

    task.host[INFOS_DATA_HOST_KEY] = system_infos
