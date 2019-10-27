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
ERROR_HEADER = "Error import [retrieve_bgp]"
HEADER_GET = "[netests - get_bgp]"
########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
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
    from tools.converters import cumulus_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def get_bgp(nr: Nornir):

    print("start get_bgp")

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    print(devices.inventory.hosts)

    path_url = f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"

    data = devices.run(
        task=generic_get,
        on_failed=True,
        num_workers=10
    )
    print_result(data)
    """
    
    #print_result(data)
    if data.failed is True:
        return False

    netests.bgp._cumulus_bgp_summary_converter(devices)
    content = open_file(path_url)
    content = (content)

    return (netests.bgp.compare_topology_and_bgp_output(content, devices))
    """

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_get(task):

    print(f"Start generic_get with {task.host.name} - {task.host.platform} - {task.host.data} {task.host.keys()} - {'connexion' in task.host.keys()}")

    use_ssh = False

    if 'nxos' in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', "") == 'ssh':
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_bgp(task)
    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and 'nxos' == task.host.platform:
            _nexus_get_bgp(task)
        else:
            _generic_napalm(task)
    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected...")

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

    print(f"Start _cumulus_get_bgp with {task.host.name}")

    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP
    )

    print(output.result)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_bgp(task):

    print(f"Start _nexus_get_bgp with {task.host.name}")

    output = task.run(
        name=f"{NEXUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_BGP
    )

    print(output.result)

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
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_bgp(task):
    raise NotImplemented

