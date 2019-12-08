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

ERROR_HEADER = "Error import [mtu_gets.py]"
HEADER_GET = "[netests - get_mtu]"

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
    from functions.mtu.mtu_converters import _napalm_mtu_converter
    from functions.mtu.mtu_converters import _ios_mtu_converter
    from functions.mtu.mtu_converters import _nexus_mtu_converter
    from functions.mtu.mtu_converters import _cumulus_mtu_converter
    from functions.mtu.mtu_converters import _iosxr_mtu_converter
    from functions.mtu.mtu_converters import _arista_mtu_converter
    from functions.mtu.mtu_converters import _juniper_mtu_converter
    from functions.mtu.mtu_converters import _extreme_vsp_mtu_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.mtu.mtu_converters")
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
def get_mtu(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")
		
    data = devices.run(
        task=generic_mtu_get,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_mtu_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or CISCO_IOS_PLATEFORM_NAME in task.host.platform or \
            JUNOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_mtu(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_mtu(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_mtu(task)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_mtu(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_mtu(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_mtu(task)
        
        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_mtu(task)

        else:
            _generic_mtu_napalm(task)

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic Napalm
#
def _generic_mtu_napalm(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_mtu(task):

    output = task.run(
        name=f"{CUMULUS_GET_MTU}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_MTU
    )
    # print_result(output)

    mtu_interfaces = _cumulus_mtu_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[MTU_DATA_HOST_KEY] = mtu_interfaces

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus (NXOS)
#
def _nexus_get_mtu(task):
    pass
	
# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_mtu(task):

    output = task.run(
            name=f"{IOS_GET_MTU}",
            task=netmiko_send_command,
            command_string=IOS_GET_MTU
    )
    #print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_interface.template")
        results_template = textfsm.TextFSM(template)
         
        parsed_results = results_template.ParseText(output.result)
        # Result Example =
        #
        #
        # type = list() of list()

        mtu_interfaces = _ios_mtu_converter(
            hostname=task.host.name,
            cmd_output=parsed_results
        )

        task.host[MTU_DATA_HOST_KEY] = mtu_interfaces


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_mtu(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_mtu(task):

    output = task.run(
        name=f"{ARISTA_GET_MTU}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_MTU
    )
    # print_result(output)

    mtu_interfaces = _arista_mtu_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result)
    )

    task.host[MTU_DATA_HOST_KEY] = mtu_interfaces

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks
#
def _juniper_get_mtu(task):
    pass
	
# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks
#
def _extreme_vsp_get_mtu(task):
    pass
    
# ----------------------------------------------------------------------------------------------------------------------
#
# Next Device
#
