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

ERROR_HEADER = "Error import [ipv4_gets.py]"
HEADER_GET = "[netests - get_ipv4]"

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
    from functions.ip.ipv4.ipv4_converters import _napalm_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _cumulus_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _nexus_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _ios_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _iosxr_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _arista_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _juniper_ipv4_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ip.ipv4.ipv4_converters")
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
    from functions.vrf.vrf_get import get_vrf_name_list
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf")
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
def get_ipv4(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(
        task=generic_ipv4_get,
        on_failed=True,
        num_workers=10
    )
    # print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_ipv4_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or CISCO_IOS_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_ipv4(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_ipv4(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_ipv4(task)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_ipv4(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_ipv4(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_ipv4(task)
        
        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_ipv4(task)

        else:
            _generic_ipv4_napalm(task)

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic IPv4 Napalm
#
def _generic_ipv4_napalm(task):

    print(f"Start _generic_ipv4_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM _generic_ipv4_napalm {task.host.platform}",
        task=napalm_get,
        getters=["get_interfaces_ip"]
    )
    # print(output.result)

    if output.result != "":
        ipv4_addresses = _napalm_ipv4_converter(task.host.name, output.result)

        task.host[IPV4_DATA_HOST_KEY] = ipv4_addresses


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_ipv4(task):

    output = task.run(
            name=f"{CUMULUS_GET_IPV4}",
            task=netmiko_send_command,
            command_string=CUMULUS_GET_IPV4
    )
    #print_result(output)

    ipv4_addresses = _cumulus_ipv4_converter(task.host.name, json.loads(output.result))

    task.host[IPV4_DATA_HOST_KEY] = ipv4_addresses

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus (NXOS)
#
def _nexus_get_ipv4(task):

    outputs_lst = list()

    output = task.run(
        name=f"{NEXUS_GET_IPV4}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_IPV4
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY]:

        if vrf != "default" and vrf != "global":
            output = task.run(
                name=NEXUS_GET_IPV4_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_IPV4_VRF.format(vrf)
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    ipv4_addresses = _nexus_ipv4_converter(task.host.name, outputs_lst)

    task.host[IPV4_DATA_HOST_KEY] = ipv4_addresses

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_ipv4(task):
    
    output = task.run(
            name=f"{IOS_GET_IPV4}",
            task=netmiko_send_command,
            command_string=IOS_GET_IPV4
    )
    #print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_interface.template")
        results_template = textfsm.TextFSM(template)
         
        parsed_results = results_template.ParseText(output.result)
        # Result Example =
        #
        #
        # type = list() of list()

    ipv4_addresses = _ios_ipv4_converter(task.host.name, parsed_results)

    task.host[IPV4_DATA_HOST_KEY] = ipv4_addresses

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_ipv4(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_ipv4(task):

    output = task.run(
            name=f"{ARISTA_GET_IPV4}",
            task=netmiko_send_command,
            command_string=ARISTA_GET_IPV4
    )
    #print_result(output)

    ipv4_addresses = _arista_ipv4_converter(task.host.name, json.loads(output.result))

    task.host[IPV4_DATA_HOST_KEY] = ipv4_addresses

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks
#
def _juniper_get_ipv4(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks
#
def _extreme_vsp_get_ipv4(task):
    pass

