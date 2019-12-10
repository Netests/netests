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
ERROR_HEADER = "Error import [ospf_gets.py]"
HEADER_GET = "[netests - get_ospf]"
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
    from functions.ospf.ospf_converters import _cumulus_ospf_converter
    from functions.ospf.ospf_converters import _nexus_ospf_converter
    from functions.ospf.ospf_converters import _arista_ospf_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.ospf.ospf_converters")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.vrf.vrf_get import get_vrf_name_list
    from functions.vrf.vrf_get import get_vrf
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.vrf.vrf_get")
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
def get_ospf(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(
        task=generic_ospf_get,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_ospf_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or ARISTA_PLATEFORM_NAME in task.host.platform:
        if 'connexion' in task.host.keys():
            if task.host.data.get('connexion', NOT_SET) == 'ssh' or task.host.get('connexion', NOT_SET):
                use_ssh = True

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _cumulus_get_ospf(task)

    elif task.host.platform == EXTREME_PLATEFORM_NAME:
        _extreme_vsp_get_ospf(task)

    elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM :
        if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
            _nexus_get_ospf(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_ospf(task)

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
        name=f"napal_get OSPF {task.host.platform}",
        task=napalm_get,
        getters=["interfaces"]
    )
    #print(output.result)

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks
#
def _cumulus_get_ospf(task):

    outputs_lst = list()

    output = task.run(
            name=f"{CUMULUS_GET_OSPF}",
            task=netmiko_send_command,
            command_string=CUMULUS_GET_OSPF
    )
    # print(output_rid.result)

    output_rid = task.run(
        name=f"{CUMULUS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_OSPF_RID
    )
    # print(output_rid.result)

    if output.result != "" and "OSPF instance does not exist" not in output.result :
        data = dict()
        data['rid'] = json.loads(output_rid.result)
        data['data'] = json.loads(output.result)

        outputs_lst.append(data)

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('ospf', NOT_SET) is True:
                output = task.run(
                    name=CUMULUS_GET_OSPF_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=CUMULUS_GET_OSPF_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)

                output_rid = task.run(
                    name=CUMULUS_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=CUMULUS_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output_rid.result)

                if output.result != "":
                    data = dict()
                    data['rid'] = json.loads(output_rid.result)
                    data['data'] = json.loads(output.result)

                    outputs_lst.append(data)

    ospf_sessions = _cumulus_ospf_converter(task.host.name, outputs_lst)

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks (VSP)
#
def _extreme_vsp_get_ospf(task):

    outputs_dict = dict()
    outputs_dict['default'] = dict()

    # Execute show ip ospf neighbors
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_neighbor.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.2.1.1', '10.255.255.201', '10.2.1.2', '1', 'Full', '0', 'Dyn', '32'],
        # ['10.2.5.1', '10.255.255.205', '10.2.5.2', '1', 'Full', '0', 'Dyn', '37']]
        # type = list() of list()
        outputs_dict['default']['neighbors'] = parsed_results

    # Execute show ip ospf interface
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_INTERFACES}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_INTERFACES
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_interface.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.2.1.1', '0.0.0.0', 'en', 'DR', '1', '1', '10.2.1.1', '10.2.1.2', 'brdc', 'none', 'dis'],
        # ['10.2.5.1', '0.0.0.0', 'en', 'BDR', '1', '1', '10.2.5.2', '10.2.5.1', 'brdc', 'none', 'dis']]
        # type = list() of list()
        outputs_dict['default']['interface'] = parsed_results

    # Execute show ip ospf
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_RID
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.255.255.102', 'enabled', '2', '100', '10', '1', '1', '1', '10']]
        # type = list() of list()
        print(parsed_results)
        outputs_dict['default']['ospf'] = parsed_results


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus NXOS
#
def _nexus_get_ospf(task):

    outputs_lst = list()

    output = task.run(
        name=f"{NEXUS_GET_OSPF}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_OSPF
    )
    # print(output.result)

    output_rid = task.run(
        name=f"{NEXUS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_OSPF_RID
    )
    # print(output_rid.result)

    if output.result != "":
        data = dict()
        data['rid'] = json.loads(output_rid.result)
        data['data'] = json.loads(output.result)

        outputs_lst.append(data)

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('ospf', NOT_SET) is True:
                output = task.run(
                    name=NEXUS_GET_OSPF_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=NEXUS_GET_OSPF_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)

                output_rid = task.run(
                    name=NEXUS_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=NEXUS_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output_rid.result)

                if output.result != "":
                    print(output.result)
                    data = dict()
                    data['rid'] = json.loads(output_rid.result)
                    data['data'] = json.loads(output.result)

                    outputs_lst.append(data)

    ospf_sessions = _nexus_ospf_converter(task.host.name, outputs_lst)

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS
#
def _cisco_get_ospf(task):
    raise NotImplemented

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vEOS
#
def _arista_get_ospf(task):

    outputs_lst = list()

    output = task.run(
        name=f"{ARISTA_GET_OSPF}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_OSPF
    )
    # print(output.result)

    output_rid = task.run(
        name=f"{ARISTA_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_OSPF_RID
    )
    # print(output_rid.result)

    if output.result != "":
        data = dict()
        data['rid'] = json.loads(output_rid.result)
        data['data'] = json.loads(output.result)

        outputs_lst.append(data)

    for vrf in task.host.get('vrfs', list()):
        if vrf.get('name', NOT_SET) in task.host[VRF_NAME_DATA_KEY]:
            if vrf.get('ospf', NOT_SET) is True:
                output = task.run(
                    name=ARISTA_GET_OSPF_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=ARISTA_GET_OSPF_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output.result)

                output_rid = task.run(
                    name=ARISTA_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET)),
                    task=netmiko_send_command,
                    command_string=ARISTA_GET_OSPF_RID_VRF.format(vrf.get('name', NOT_SET))
                )
                # print(output_rid.result)

                if output.result != "" and "OSPF instance does not exist" not in output.result:
                    print(output.result)
                    data = dict()
                    data['rid'] = json.loads(output_rid.result)
                    data['data'] = json.loads(output.result)

                    outputs_lst.append(data)

    ospf_sessions = _arista_ospf_converter(task.host.name, outputs_lst)

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _junos_get_ospf(task):
    raise NotImplemented

