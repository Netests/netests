#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import json
import textfsm
from nornir.core import Nornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command, napalm_get
from functions.vrf.vrf_get import get_vrf_name_list, get_vrf
from functions.bgp.bgp_converters import (
    _cumulus_bgp_converter,
    _nexus_bgp_converter,
    _ios_bgp_converter,
    _arista_bgp_converter,
    _juniper_bgp_converter,
    _extreme_vsp_bgp_converter,
)
from const.constants import (
    NOT_SET,
    TEXTFSM_PATH,
    VRF_NAME_DATA_KEY,
    BGP_SESSIONS_HOST_KEY,
    NEXUS_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    ARISTA_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    NAPALM_COMPATIBLE_PLATEFORM,
    CUMULUS_GET_BGP,
    CUMULUS_GET_BGP_VRF,
    EXTREME_VSP_GET_BGP,
    EXTREME_VSP_GET_BGP_VRF,
    NEXUS_GET_BGP,
    NEXUS_GET_BGP_VRF,
    IOS_GET_BGP,
    IOS_GET_BGP_VRF,
    ARISTA_GET_BGP,
    ARISTA_GET_BGP_VRF,
    JUNOS_GET_BGP,
    JUNOS_GET_BGP_RID,
    JUNOS_GET_BGP_VRF,
    JUNOS_GET_BGP_VRF_RID,
)


ERROR_HEADER = "Error import [bgp_gets.py]"
HEADER_GET = "[netests - get_bgp]"


def get_bgp(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf_name_list(nr)

    data = devices.run(task=generic_bgp_get, on_failed=True, num_workers=10)


def generic_bgp_get(task):

    if BGP_SESSIONS_HOST_KEY not in task.host.keys():

        use_ssh = False

        if (
            NEXUS_PLATEFORM_NAME in task.host.platform
            or JUNOS_PLATEFORM_NAME in task.host.platform
            or ARISTA_PLATEFORM_NAME in task.host.platform
            or CISCO_IOSXR_PLATEFORM_NAME in task.host.platform
            or CISCO_IOS_PLATEFORM_NAME in task.host.platform
        ):
            if "connexion" in task.host.keys():
                if (
                    task.host.data.get("connexion", NOT_SET) == "ssh" or
                    task.host.get("connexion", NOT_SET)
                ):
                    use_ssh = True

        if task.host.platform == CUMULUS_PLATEFORM_NAME:
            _cumulus_get_bgp(task)

        elif task.host.platform == EXTREME_PLATEFORM_NAME:
            _extreme_vsp_get_bgp(task)

        elif task.host.platform in NAPALM_COMPATIBLE_PLATEFORM:
            if use_ssh and NEXUS_PLATEFORM_NAME == task.host.platform:
                _nexus_get_bgp(task)

            if use_ssh and CISCO_IOS_PLATEFORM_NAME == task.host.platform:
                _ios_get_bgp(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _iosxr_get_bgp(task)

            elif use_ssh and ARISTA_PLATEFORM_NAME == task.host.platform:
                _arista_get_bgp(task)

            elif use_ssh and JUNOS_PLATEFORM_NAME == task.host.platform:
                _juniper_get_bgp(task)

            else:
                _generic_bgp_napalm(task)

        else:
            # RAISE EXCEPTIONS
            print(f"{HEADER_GET} No plateform selected for {task.host.name}.")


def _generic_bgp_napalm(task):

    print(f"Start _generic_bgp_napalm with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_bgp_neighbors"],
    )
    # print(output.result)

    if output.result != "":
        bgp_sessions = _napalm_bgp_converter(task.host.name, output.result)

        task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


def _cumulus_get_bgp(task):

    outputs_lst = list()

    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP,
    )
    # print(output.result)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default" and vrf != "global":

            output = task.run(
                name=CUMULUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_BGP_VRF.format(vrf),
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    bgp_sessions = _cumulus_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


def _extreme_vsp_get_bgp(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{EXTREME_VSP_GET_BGP}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_BGP,
    )
    # print_result(output)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_bgp_summary.textfsm"
        )
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['4', '65100', '10.255.255.102', '10.2.5.2', '65205', 'Established',
        #   '180', '60', '180', '60', '100', '120', '5', '0', '00', '42', '05']
        # ['4', '65100', '', '10.255.255.205', '65205', 'Established',
        #   '180', '60', '180', '60', '100', '3', '5', '0', '00', '42', '05'],
        # ['4', '65100', '', '', '', '', '', '', ... , '', '', '', '', '']]
        # type = list() of list()
        # Last line is empty ....
        outputs_dict["default"] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default" and vrf != "GlobalRouter":

            output = task.run(
                name=EXTREME_VSP_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_BGP_VRF.format(vrf),
            )
            # print_result(output)

            if (
                output.result != ""
                and "BGP instance does not exist for" not in output.result
            ):
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_bgp_summary.textfsm"
                )
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # Result Example = [
                # ['4', '65100', '10.0.5.102', '10.0.5.202', '65202', 'Idle',
                #   '0', '0', '180', '60', '100', '120',
                #   '5', '16', '10', '40', '50'],
                # ['4', '65100', '', '', '', '', ..... , '', '', '', '']]
                # type = list() of list()
                # Last line is empty ....
                outputs_dict[vrf] = parsed_results

    bgp_sessions = _extreme_vsp_bgp_converter(task.host.name, outputs_dict)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


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

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "global":
            output = task.run(
                name=NEXUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_BGP_VRF.format(vrf),
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    bgp_sessions = _nexus_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


def _ios_get_bgp(task):

    outputs_dict = dict()

    output = task.run(
        name=f"{IOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=IOS_GET_BGP
    )
    # print_result(output)

    if output.result != "":
        template = open(f"{TEXTFSM_PATH}cisco_ios_show_ip_bgp_summary.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)
        # Result Example = [
        # ['10.255.255.205', '65205', '10.0.0.1', '65100', '00:33:09', '2'],
        # ['10.255.255.205', '65205', '10.2.2.1', '65535', 'never', 'Idle']]
        # type = list() of list()
        outputs_dict["default"] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default":

            output = task.run(
                name=IOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=IOS_GET_BGP_VRF.format(vrf),
            )
            # print_result(output)

            if output.result != "":
                template = open(
                    f"{TEXTFSM_PATH}cisco_ios_show_ip_bgp_summary.textfsm"
                )
                results_template = textfsm.TextFSM(template)

                parsed_results = results_template.ParseText(output.result)
                # Result Example = [
                # type = list() of list()
                outputs_dict[vrf] = parsed_results

    bgp_sessions = _ios_bgp_converter(task.host.name, outputs_dict)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


def _iosxr_get_bgp(task):
    pass


def _arista_get_bgp(task):

    outputs_lst = list()

    output = task.run(
        name=f"{ARISTA_GET_BGP}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_BGP,
    )
    # print_result(output)

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "global":
            output = task.run(
                name=ARISTA_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_BGP_VRF.format(vrf),
            )
            # print(output.result)

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    bgp_sessions = _arista_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions


def _juniper_get_bgp(task):

    outputs_lst = dict()
    outputs_lst["default"] = dict()

    output = task.run(
        name=f"{JUNOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_BGP
    )
    # print_result(output)

    if output.result != "":
        outputs_lst["default"]["bgp"] = json.loads(output.result)

        output = task.run(
            name=f"{JUNOS_GET_BGP_RID}",
            task=netmiko_send_command,
            command_string=JUNOS_GET_BGP_RID,
        )
        # print_result(output)

        if output.result != "":
            outputs_lst["default"]["conf"] = json.loads(output.result)

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf != "default":

            output = task.run(
                name=JUNOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_BGP_VRF.format(vrf),
            )
            # print(output.result)

            if output.result != "" and "bgp-peer" in output.result:
                outputs_lst[vrf] = dict()
                outputs_lst[vrf]["bgp"] = json.loads(output.result)

                output = task.run(
                    name=JUNOS_GET_BGP_VRF_RID.format(vrf),
                    task=netmiko_send_command,
                    command_string=JUNOS_GET_BGP_VRF_RID.format(vrf),
                )
                # print(output.result)

                if output.result != "" and "router-id" in output.result:
                    outputs_lst[vrf]["conf"] = json.loads(output.result)

    bgp_sessions = _juniper_bgp_converter(task.host.name, outputs_lst)

    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
