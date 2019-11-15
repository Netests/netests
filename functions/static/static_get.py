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
ERROR_HEADER = "Error import [static_gets.py]"
HEADER_GET = "[netests - static_gets]"
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
    from functions.static.static_converters import _cumulus_static_converter
    from functions.static.static_converters import _nexus_static_converter
    from functions.static.static_converters import _arista_static_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.static.static_converters")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.vrf.vrf_get import get_vrf_name_list
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
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
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    exit(EXIT_FAILURE)
    print(importError)

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
def get_static(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(
        task=generic_static_get,
        on_failed=True,
        num_workers=10
    )
    print_result(data)


# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_static_get(task):

    if STATIC_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform:
            if 'connexion' in task.host.keys():
                if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_static(task)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_static(task)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_static(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_static(task)

            else:
                _generic_static_napalm(task)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}...")


# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_static_napalm(task):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_static(task):

    outputs_lst = list()

    output = task.run(
        name=f"{CUMULUS_GET_STATIC}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_STATIC
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY]:

        if vrf != "default" and vrf != "global":
            output = task.run(
                name=CUMULUS_GET_STATIC_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_STATIC_VRF.format(vrf)
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    static_routes = _cumulus_static_converter(task.host.name, outputs_lst, task.host[VRF_NAME_DATA_KEY])

    task.host[STATIC_DATA_HOST_KEY] = static_routes


# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_static(task):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_static(task):

    outputs_lst = list()

    output = task.run(
        name=f"{NEXUS_GET_STATIC}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_STATIC
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY]:

        if vrf != "default" and vrf != "global":
            output = task.run(
                name=NEXUS_GET_STATIC_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_STATIC_VRF.format(vrf)
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    static_routes = _nexus_static_converter(task.host.name, outputs_lst)

    task.host[STATIC_DATA_HOST_KEY] = static_routes

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _cisco_get_static(task):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_static(task):

    outputs_lst = list()

    output = task.run(
        name=f"{ARISTA_GET_STATIC}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_STATIC
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY]:

        if vrf != "default" and vrf != "global":
            output = task.run(
                name=ARISTA_GET_STATIC_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_STATIC_VRF.format(vrf)
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    static_routes = _arista_static_converter(task.host.name, outputs_lst)

    task.host[STATIC_DATA_HOST_KEY] = static_routes


# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_static(task):
    pass