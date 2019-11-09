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
ERROR_HEADER = "Error import [bgp_gets.py]"
HEADER_GET = "[netests - get_bgp]"
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
    from functions.bgp.bgp_converters import _napalm_bgp_converter
    from functions.bgp.bgp_converters import _cumulus_bgp_converter
    from functions.bgp.bgp_converters import _nexus_bgp_converter
    from functions.bgp.bgp_converters import _arista_bgp_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_get import get_vrf_name_list
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp_converters")
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
def get_bgp(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(
        task=generic_bgp_get,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_bgp_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', "") == 'ssh':
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_bgp(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_bgp(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_bgp(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_bgp(task)

        else:
            _generic_napalm(task)

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_napalm(task):

    print(f"Start _generic_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_bgp_neighbors"]
    )
    #print(output.result)

    if output.result != "":
        bgp_sessions = _napalm_bgp_converter(task.host.name, output.result)

        task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_bgp(task):

    outputs_lst = list()

    output = task.run(
            name=f"{CUMULUS_GET_BGP}",
            task=netmiko_send_command,
            command_string=CUMULUS_GET_BGP
    )
    #print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('bgp', NOT_SET) is True:
                output = task.run(
                    name=CUMULUS_GET_BGP_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=CUMULUS_GET_BGP_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)

                if output.result != "":
                    outputs_lst.append(json.loads(output.result))

    bgp_sessions = _cumulus_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_bgp(task):

    output = task.run(
        name=f"LSODHOUEWHDUWEHDZWEDOUZWQEGDOUWEVDOUWEQVDUWEVDOUWEZDVWOEUZVDOUWEZVDWEOZDVOUWEQZDVOWEUQZDVWDZWE",
        task=netmiko_send_command,
        command_string="COMMANDE à DEFINIR !!!!!!"
    )
    #print(output.result)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_bgp(task):

    outputs_lst = list()

    output = task.run(
        name=f"{NEXUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_BGP
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('bgp', NOT_SET) is True:
                output = task.run(
                    name=NEXUS_GET_BGP_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=NEXUS_GET_BGP_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)
                if output.result != "":
                    outputs_lst.append(json.loads(output.result))

    bgp_sessions = _nexus_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _cisco_get_bgp(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_bgp(task):

    outputs_lst = list()

    output = task.run(
        name=f"{ARISTA_GET_BGP}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_BGP
    )
    #print_result(output)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('bgp', NOT_SET) is True:
                output = task.run(
                    name=ARISTA_GET_BGP_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=ARISTA_GET_BGP_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)

                if output.result != "":
                    outputs_lst.append(json.loads(output.result))

    bgp_sessions = _arista_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_bgp(task):
    raise NotImplemented

