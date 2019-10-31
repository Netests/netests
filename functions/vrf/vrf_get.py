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
ERROR_HEADER = "Error import [vrf_gets.py]"
HEADER_GET = "[netests - vrf_gets]"
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
    from protocols.vrf import VRF, ListVRF
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
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#
def check_vrf_exist(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    path_url = f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"

    data = devices.run(
        task=generic_vrf_get,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_vrf_get(task):

    print(
        f"Start generic_get with {task.host.name} - {task.host.platform} - {task.host.data} {task.host.keys()} - {'connexion' in task.host.keys()}")

    use_ssh = False

    if 'nxos' in task.host.platform or 'eos' in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', "") == 'ssh':
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_vrf_name(task)
    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_vrf_name(task)
    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM:
        if use_ssh and 'nxos' == task.host.platform:
            _nexus_get_vrf_name(task)
        elif use_ssh and 'eos' == task.host.platform:
            _arista_get_vrf_name(task)
        else:
            _generic_napalm_vrf_name(task)
    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Network NXOS
#
def _cumulus_get_vrf_name(task):

    output = task.run(
        name=f"{CUMULUS_GET_VRF}",
        task=netmiko_send_command,
        command_string=f"{CUMULUS_GET_VRF}",
    )

    template = open(
        f"{TEXTFSM_PATH}cumulus_net_show_vrf.template")
    results_template = textfsm.TextFSM(template)

    print(results_template)

    parsed_results = results_template.ParseText(output.result)

    print((output.result))
    print(parsed_results)
    list_vrf = ListVRF(list())

    for line in parsed_results:
        vrf = VRF(
            vrf_name=line[0],
            vrf_id = line[1]
        )

        list_vrf.vrf_lst.append(vrf)

    print(list_vrf)
    task.host[VRF_DATA_KEY] = list_vrf

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus
#
def _nexus_get_vrf_name(task):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_vrf_name(task):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Network (VSP)
#
def _extreme_vsp_get_vrf_name(task):
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_napalm_vrf_name(task):
    pass
