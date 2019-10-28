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
    from functions.bgp_converters import _cumulus_bgp_converter
    from functions.bgp_converters import _nexus_bgp_converter
    from functions.bgp_converters import _arista_bgp_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp_converters")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def get_bgp(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    path_url = f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"

    data = devices.run(
        task=generic_get,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_get(task):

    print(f"Start generic_get with {task.host.name} - {task.host.platform} - {task.host.data} {task.host.keys()} - {'connexion' in task.host.keys()}")

    use_ssh = False

    if 'nxos' in task.host.platform or 'eos' in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', "") == 'ssh':
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_bgp(task)
    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_bgp(task)
    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and 'nxos' == task.host.platform:
            _nexus_get_bgp(task)
        elif use_ssh and 'eos' == task.host.platform:
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
        name=f"napal_get bgp {task.host.platform}",
        task=napalm_get,
        getters=["interfaces"])

    print(output.result)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Network
#
def _cumulus_get_bgp(task):

    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP
    )
    #print(output.result)

    bgp_sessions = _cumulus_bgp_converter(task.host.name, output.result)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Network (VSP)
#
def _extreme_vsp_get_bgp(task):

    output = task.run(
        name=f"LSODHOUEWHDUWEHDZWEDOUZWQEGDOUWEVDOUWEQVDUWEVDOUWEZDVWOEUZVDOUWEZVDWEOZDVOUWEQZDVOWEUQZDVWDZWE",
        task=netmiko_send_command,
        command_string="COMMANDE à DEFINIR !!!!!!"
    )
    print(output.result)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_bgp(task):

    output = task.run(
        name=f"{NEXUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_BGP
    )
    # print(output.result)

    bgp_sessions = _nexus_bgp_converter(task.host.name, output.result)

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

    output = task.run(
        name=f"{ARISTA_GET_BGP}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_BGP
    )
    #print_result(output)

    bgp_sessions = _arista_bgp_converter(task.host.name, output.result)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_bgp(task):
    raise NotImplemented

