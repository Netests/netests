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
    print(importError)
    exit(EXIT_FAILURE)

try:
    from protocols.vrf import VRF, ListVRF
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vrf")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_converter import _napalm_vrf_converter
    from functions.vrf.vrf_converter import _cumulus_vrf_converter
    from functions.vrf.vrf_converter import _nexus_vrf_converter
    from functions.vrf.vrf_converter import _arista_vrf_converter
    from functions.vrf.vrf_converter import _juniper_vrf_converter
    from functions.vrf.vrf_converter import _iosxr_vrf_converter
    from functions.vrf.vrf_converter import _ios_vrf_converter
    from functions.vrf.vrf_converter import _extreme_vsp_vrf_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf.vrf_converter")
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
def get_vrf(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=generic_vrf_get,
        function="GET",
        on_failed=True,
        num_workers=10
    )
    # print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Get list of vrf name for each devices
#
def get_vrf_name_list(nr: Nornir, function="LIST"):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    path_url = f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"

    data = devices.run(
        task=generic_vrf_get,
        function=function,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_vrf_get(task, function="GET"):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or JUNOS_PLATEFORM_NAME in task.host.platform or \
            ARISTA_PLATEFORM_NAME in task.host.platform or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOS_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        if function == 'GET':
            _cumulus_get_vrf(task)
        elif function == 'LIST':
            _get_vrf_name_list(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        if function == 'GET':
            _extreme_vsp_get_vrf(task)
        elif function == 'LIST':
            _get_vrf_name_list(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        if function == 'GET':
            _extreme_vsp_get_vrf(task)
        elif function == 'LIST':
            _get_vrf_name_list(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM:
        # Nexus get_network_instances is not Implemented by NAPALM (November 2019)
        # File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/napalm/base/base.py", line 1535, in get_network_instances
        # raise NotImplementedError
        #   NotImplementedError
        if NEXUS_PLATEFORM_NAME == task.host.platform:
            port = task.host.port
            task.host.port = 22
            if function == 'GET':
                _nexus_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)
            task.host.port = port

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            if function == 'GET':
                _arista_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)

        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            if function == 'GET':
                _juniper_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            if function == 'GET':
                _iosxr_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            if function == 'GET':
                _ios_get_vrf(task)
            elif function == 'LIST':
                _get_vrf_name_list(task)

        else:
            _generic_napalm_vrf(task)
    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")


# ----------------------------------------------------------------------------------------------------------------------
#
def _get_vrf_name_list(task):

    vrf_name_lst = dict()

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_vrf(task)
    elif task.host.platform == NEXUS_PLATEFORM_NAME:
        _nexus_get_vrf(task)
    elif task.host.platform == ARISTA_PLATEFORM_NAME:
        _arista_get_vrf(task)
    elif task.host.platform == JUNOS_PLATEFORM_NAME:
        _juniper_get_vrf(task)
    elif task.host.platform == CISCO_IOSXR_PLATEFORM_NAME:
        _iosxr_get_vrf(task)
    elif task.host.platform == CISCO_IOS_PLATEFORM_NAME:
        _ios_get_vrf(task)
    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_vrf(task)

    for vrf in task.host[VRF_DATA_KEY].vrf_lst:
        vrf_name_lst[vrf.vrf_name] = vrf.vrf_id

    task.host[VRF_NAME_DATA_KEY] = vrf_name_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Network NXOS
#
def _cumulus_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{CUMULUS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{CUMULUS_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}cumulus_net_show_bgp_vrf.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)

        list_vrf = ListVRF(list())

        for line in parsed_results:
            vrf = VRF(
                vrf_name=line[0],
                vrf_id = line[1]
            )

            list_vrf.vrf_lst.append(vrf)

        task.host[VRF_DATA_KEY] = list_vrf

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus
#
def _nexus_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{NEXUS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{NEXUS_GET_VRF}",
        )

        vrf_list = _nexus_vrf_converter(task.host.name, json.loads(output.result))

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{ARISTA_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{ARISTA_GET_VRF}",
        )

        vrf_list = _arista_vrf_converter(task.host.name, json.loads(output.result))

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_vrf(task):
    
    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{EXTREME_VSP_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{EXTREME_VSP_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_vrf.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)

        vrf_list = _extreme_vsp_vrf_converter(task.host.name, parsed_results)

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Networks (Junos)
#
def _juniper_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{JUNOS_GET_VRF_DETAIL}",
            task=netmiko_send_command,
            command_string=f"{JUNOS_GET_VRF_DETAIL}",
        )

        vrf_list = _juniper_vrf_converter(task.host.name, json.loads(output.result))

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOSXR
#
def _iosxr_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{IOSXR_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{IOSXR_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}cisco_xr_show_vrf_detail.template")
        results_template = textfsm.TextFSM(template)

        # Return value
        # Example : [['mgmt', '1', '<not set>'], ['tenant-1', '2', '10.255.255.103:103']]

        parsed_results = results_template.ParseText(output.result)

        vrf_list = _iosxr_vrf_converter(task.host.name, parsed_results)

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _ios_get_vrf(task):

    if VRF_DATA_KEY not in task.host.keys():

        output = task.run(
            name=f"{IOS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{IOS_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}cisco_xr_show_vrf_detail.template")
        results_template = textfsm.TextFSM(template)

        # Return value
        # Example : [['mgmt', '1', '<not set>'], ['tenant-1', '2', '10.255.255.103:103']]

        parsed_results = results_template.ParseText(output.result)

        vrf_list = _ios_vrf_converter(task.host.name, parsed_results)

        task.host[VRF_DATA_KEY] = vrf_list

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_napalm_vrf(task):

    print(f"Start _generic_napalm_vrf with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_network_instances"]
    )
    # print(output.result)

    if output.result != "":
        vrf_list = _napalm_vrf_converter(task.host.name, output.result)

        task.host[VRF_DATA_KEY] = vrf_list

