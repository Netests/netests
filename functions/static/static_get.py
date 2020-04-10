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
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.static.static_converters import _napalm_static_converter
    from functions.static.static_converters import _cumulus_static_converter
    from functions.static.static_converters import _nexus_static_converter
    from functions.static.static_converters import _arista_static_converter
    from functions.static.static_converters import _ios_static_converter
    from functions.static.static_converters import _extreme_vsp_static_converter
    from functions.static.static_converters import _juniper_static_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.static.static_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
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
    exit(EXIT_FAILURE)
    print(importError)

try:
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def get_static(nr: Nornir, filters={}, level=None, own_vars={}):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf(nr)

    data = devices.run(
        task=generic_static_get,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)


# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_static_get(task):

    if STATIC_DATA_HOST_KEY not in task.host.keys():

        use_ssh = False

        if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
                JUNOS_PLATEFORM_NAME in task.host.platform or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or \
                CISCO_IOS_PLATEFORM_NAME in task.host.platform:
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

            elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
                _iosxr_get_static(task)

            elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
                _ios_get_static(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_static(task)

            elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
                _juniper_get_static(task)

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

    """
    print(f"Start _generic_static_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_route_to {task.host.platform}",
        task=napalm_get,
        getters=["get_route_to"]
    )
    # print(output.result)

    if output.result != "":
        static_routes = _napalm_static_converter(
            hostname=task.host.name,
            cmd_outputs=output.result
        )

        task.host[STATIC_DATA_HOST_KEY] = static_routes
    """
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

    outputs_dict = dict()

    output = task.run(
        name=f"{EXTREME_VSP_GET_STATIC}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_STATIC
    )

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_route_static.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example =[
        # ['1.1.1.1', '255.255.255.255', '10.2.1.2', 'GlobalRouter', '1', '5', 'TRUE', 'ACTIVE', 'TRUE']]
        # type = list() of list()
        outputs_dict['default'] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default" and vrf != "GlobalRouter":

            output = task.run(
                name=EXTREME_VSP_GET_STATIC_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_STATIC_VRF.format(vrf)
            )
            # print_result(output)

            if output.result != "":
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_route_static.textfsm")
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # Result Example = [
                # ['0.0.0.0', '0.0.0.0', '10.0.5.1', 'MgmtRouter', '1', '5', 'TRUE', 'ACTIVE', 'TRUE']]
                # type = list() of list()
                outputs_dict[vrf] = parsed_results

    static_routes = _extreme_vsp_static_converter(outputs_dict)

    task.host[STATIC_DATA_HOST_KEY] = static_routes


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
def _ios_get_static(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{IOS_GET_STATIC}",
        task=netmiko_send_command,
        command_string=IOS_GET_STATIC
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_route_static.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example =[
        # ['10.8.0.0', '', '', '24', 'GigabitEthernet0/1'], ['10.8.0.64', '', '', '26', 'GigabitEthernet0/7'],
        # ['10.8.0.128', '1', '0', '26', '10.1.5.1'], ['10.255.255.101', '1', '0', '32', '10.1.5.1']]
        # type = list() of list()
        outputs_dict['default'] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default":

            output = task.run(
                name=IOS_GET_STATIC_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=IOS_GET_STATIC_VRF.format(vrf)
            )
            # print_result(output)

            if output.result != "":
                template = open(
                    f"{TEXTFSM_PATH}cisco_ios_show_ip_route_static.textfsm")
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # Result Example = [
                # type = list() of list()
                outputs_dict[vrf] = parsed_results

    static_routes = _ios_static_converter(outputs_dict)

    task.host[STATIC_DATA_HOST_KEY] = static_routes

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_static(task):
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
def _juniper_get_static(task):

    output = task.run(
        name=f"{JUNOS_GET_STATIC}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_STATIC
    )
    # print(output.result)

    if output.result != "":

        static_routes = _juniper_static_converter(
            hostname=task.host.name,
            cmd_outputs=json.loads(output.result)
        )

        task.host[STATIC_DATA_HOST_KEY] = static_routes
