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
    from functions.ospf.ospf_converters import _extreme_vsp_ospf_converter
    from functions.ospf.ospf_converters import _ios_ospf_converter
    from functions.ospf.ospf_converters import _juniper_ospf_converter
    from functions.ospf.ospf_converters import _napalm_ospf_converter
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
    #print_result(data)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def generic_ospf_get(task):

    use_ssh = False

    if NEXUS_PLATEFORM_NAME in task.host.platform or JUNOS_PLATEFORM_NAME in task.host.platform or \
            ARISTA_PLATEFORM_NAME in task.host.platform or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform or \
            CISCO_IOS_PLATEFORM_NAME in task.host.platform:
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

        elif use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
            _ios_get_ospf(task)

        elif use_ssh and CISCO_IOSXR_PLATEFORM_NAME == task.host.platform:
            _iosxr_get_ospf(task)

        elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
            _arista_get_ospf(task)

        elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
            _juniper_get_ospf(task)

        else:
            _generic_ospf_napalm(task)

    else:
        # RAISE EXCEPTIONS
        print(f"{HEADER_GET} No plateform selected for {task.host.name}...")

# ----------------------------------------------------------------------------------------------------------------------
#
# Function for devices which are compatible with NAPALM
#
def _generic_ospf_napalm(task):
    pass
    """
    print(f"Start _generic_ospf_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_ospf_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_ospf_neighbors"]
    )
    # print(output.result)

    if output.result != "":
        bgp_sessions = _napalm_ospf_converter(
            task.host.name,
            output.result
        )

        task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
    """

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

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "global":
            output = task.run(
                name=CUMULUS_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_OSPF_VRF.format(vrf)
            )
            # print(output.result)

            output_rid = task.run(
                name=CUMULUS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_OSPF_RID_VRF.format(vrf)
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
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_neighbor.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.2.1.1', '10.255.255.201', '10.2.1.2', '1', 'Full', '0', 'Dyn', '32'],
        # ['10.2.5.1', '10.255.255.205', '10.2.5.2', '1', 'Full', '0', 'Dyn', '37']]
        # type = list() of list()
        outputs_dict['default'][OSPF_NEI_KEY] = parsed_results

    # Execute show ip ospf interface
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_INTERFACES}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_INTERFACES
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_interface.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.2.1.1', '0.0.0.0', 'en', 'DR', '1', '1', '10.2.1.1', '10.2.1.2', 'brdc', 'none', 'dis'],
        # ['10.2.5.1', '0.0.0.0', 'en', 'BDR', '1', '1', '10.2.5.2', '10.2.5.1', 'brdc', 'none', 'dis']]
        # type = list() of list()
        outputs_dict['default'][OSPF_INT_KEY] = parsed_results

    # Execute show ip ospf
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_RID
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.255.255.102', 'enabled', '2', '100', '10', '1', '1', '1', '10']]
        # type = list() of list()
        outputs_dict['default'][OSPF_RIB_KEY] = parsed_results

    # Execute show ip interfaces to have OSPF neighbors inteface name
    output = task.run(
        name=f"{EXTREME_VSP_GET_IPV4}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_IPV4
    )
    # print_result(output)

    if output.result != "" and "All 0 out of 0" not in output.result:
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_interface.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        #
        # type = list() of list()
        outputs_dict['default'][OSPF_INT_NAME_KEY] = parsed_results


    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "GlobalRouter":

            # Execute show ip ospf neighbors vrf "vrf"
            output = task.run(
                name=EXTREME_VSP_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_VRF.format(vrf)
            )
            # print_result(output)

            if output.result != "" and "OSPF instance does not exist" not in output.result:
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_neighbor.textfsm")
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # type = list() of list()
                outputs_dict[vrf] = dict()
                outputs_dict[vrf][OSPF_NEI_KEY] = parsed_results


            # Execute show ip ospf interface vrf "vrf"
            output = task.run(
                name=EXTREME_VSP_GET_OSPF_INTERFACES_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_INTERFACES_VRF.format(vrf)
            )
            # print_result(output)

            if output.result != "" and "OSPF instance does not exist" not in output.result:
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_interface.textfsm")
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # type = list() of list()
                outputs_dict[vrf][OSPF_INT_KEY] = parsed_results


            # Execute show ip ospf vrf "vrf"
            output = task.run(
                name=EXTREME_VSP_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_RID_VRF.format(vrf)
            )
            # print_result(output)

            if output.result != "" and "OSPF instance does not exist" not in output.result:
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf.textfsm")
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # type = list() of list()
                outputs_dict[vrf][OSPF_RIB_KEY] = parsed_results

            if vrf in outputs_dict.keys():
                # Execute show ip interfaces to have OSPF neighbors inteface name
                output = task.run(
                    name=EXTREME_VSP_GET_IPV4_VRF.format(vrf),
                    task=netmiko_send_command,
                    command_string=EXTREME_VSP_GET_IPV4_VRF.format(vrf)
                )
                # print_result(output)

                if output.result != "" and "All 0 out of 0" not in output.result:
                    template = open(
                        f"{TEXTFSM_PATH}extreme_vsp_show_ip_interface.textfsm")
                    results_template = textfsm.TextFSM(template)

                    parsed_results = results_template.ParseText(output.result)
                    # Result Example = [
                    #
                    # type = list() of list()
                    outputs_dict[vrf][OSPF_INT_NAME_KEY] = parsed_results

    ospf_sessions = _extreme_vsp_ospf_converter(
        hostname=task.host.name,
        cmd_outputs=outputs_dict
    )

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions

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

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "GlobalRouter":
            output = task.run(
                name=NEXUS_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_OSPF_VRF.format(vrf)
            )
            # print(output.result)

            output_rid = task.run(
                name=NEXUS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_OSPF_RID_VRF.format(vrf)
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
def _ios_get_ospf(task):

    outputs_dict = dict()

    # Execute show ip ospf
    output = task.run(
        name=f"{IOS_GET_OSPF}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['1', '10.255.255.205', ''],
        # ['2', '205.205.205.205', 'mgmt']]
        # type = list() of list()
        outputs_dict[OSPF_RIB_KEY] = parsed_results


    # Execute show ip ospf neighbor detail
    output = task.run(
        name=f"{IOS_GET_OSPF_NEI}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF_NEI
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf_neighbor_detail.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.255.255.102', '10.2.5.1', '0', 'GigabitEthernet0/2', 'FULL', '10.2.5.2', '10.2.5.1', '10', '12', '34'],
        # ['10.0.5.101', '10.0.5.101', '0.0.0.100', 'GigabitEthernet0/0', 'FULL', '10.0.5.205', '10.0.5.201', '01', '12', '31']]
        # type = list() of list()
        outputs_dict[OSPF_NEI_KEY] = parsed_results

    # Execute show ip ospf interface
    output = task.run(
        name=f"{IOS_GET_OSPF_INT}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF_INT
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf_interface_brief.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [['Gi0/1', '1', '0', '10.1.5.2/30', '1', 'DR', '0/0'],
        # ['Gi0/0', '2', '0.0.0.100', '10.0.5.205/24', '1', 'DR', '2/2']]
        # type = list() of list()
        outputs_dict[OSPF_INT_KEY] = parsed_results

    ospf_sessions = _ios_ospf_converter(
        hostname=task.host.name,
        cmd_outputs=outputs_dict
    )

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS-XR
#
def _iosxr_get_ospf(task):
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

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "GlobalRouter":

            output = task.run(
                name=ARISTA_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_OSPF_VRF.format(vrf)
            )
            # print(output.result)

            output_rid = task.run(
                name=ARISTA_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_OSPF_RID_VRF.format(vrf)
            )
            # print(output_rid.result)

            if output.result != "" and "OSPF instance does not exist" not in output.result:
                data = dict()
                data['rid'] = json.loads(output_rid.result)
                data['data'] = json.loads(output.result)

                outputs_lst.append(data)

    ospf_sessions = _arista_ospf_converter(
        hostname=task.host.name,
        cmd_outputs=outputs_lst
    )

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper JunOS
#
def _juniper_get_ospf(task):

    outputs_dict = dict()

    # Execute show ospf neighbor detail
    output_nei = task.run(
        name=f"{JUNOS_GET_OSPF_NEI}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_OSPF_NEI
    )
    # print_result(output)

    outputs_dict['default'] = dict()

    if output_nei.result != "" and "OSPF instance is not running" not in output_nei.result:
        outputs_dict['default'][OSPF_NEI_KEY] = json.loads(output_nei.result)


    # Execute show ospf overview
    output_rid = task.run(
        name=f"{JUNOS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_OSPF_RID
    )
    # print_result(output)

    if output_rid.result != "" and "OSPF instance is not running" not in output_rid.result:
        outputs_dict['default'][OSPF_RIB_KEY] = json.loads(output_rid.result)


    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "master":

            # Execute show ospf neighbor detail
            output_nei = task.run(
                name=JUNOS_GET_OSPF_NEI_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_OSPF_NEI_VRF.format(vrf)
            )
            # print_result(output)



            if output_nei.result != "" and "OSPF instance is not running" not in output_nei.result:
                outputs_dict[vrf] = dict()
                outputs_dict[vrf][OSPF_NEI_KEY] = json.loads(output_nei.result)

            # Execute show ospf overview
            output_rid = task.run(
                name=JUNOS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_OSPF_RID_VRF.format(vrf)
            )
            # print_result(output)

            if output_rid.result != "" and "OSPF instance is not running" not in output_rid.result:
                outputs_dict[vrf][OSPF_RIB_KEY] = json.loads(output_rid.result)


    ospf_sessions = _juniper_ospf_converter(
        hostname=task.host.name,
        cmd_outputs=outputs_dict
    )

    task.host[OSPF_SESSIONS_HOST_KEY] = ospf_sessions