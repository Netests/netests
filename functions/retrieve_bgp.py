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
    
    """
    
    #print_result(data)
    if data.failed is True:
        return False

    netests.bgp._cumulus_bgp_summary_converter(devices)
    content = open_file(path_url)
    content = (content)

    return (netests.bgp.compare_topology_and_bgp_output(content, devices))
    """

def generic_get(task):

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_bgp(task)
    elif task.host.platform == NEXUS_PLATEFORM_NAME:
        _nexus_get_bgp(task)
    elif task.host.platform == CISCO_PLATEFORM_NAME:
        _cisco_get_bgp(task)
    elif task.host.platform == ARISTA_PLATEFORM_NAME:
        _arista_get_bgp(task)
    elif task.host.platform == JUNOS_PLATEFORM_NAME:
        _junos_get_bgp(task)
    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected...")


def _cumulus_get_bgp(task):
    print(f"Start _nexus_get_bgp with {task.host.name}")

    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP
    )

    print(output.result)

def _nexus_get_bgp(task):
    print(f"Start _nexus_get_bgp with {task.host.name}")
    pass

def _cisco_get_bgp(task):
    print(f"Start _cisco_get_bgp with {task.host.name}")
    pass

def _arista_get_bgp(task):
    print(f"Start _arista_get_bgp with {task.host.name}")
    pass

def _junos_get_bgp(task):
    print(f"Start _junos_get_bgp with {task.host.name}")
    pass

