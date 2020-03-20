#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    TEXTFSM_PATH,
    BGP_SESSIONS_HOST_KEY,
    IOS_GET_BGP,
    IOS_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.bgp_converters import (
    _ios_bgp_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
)


def _ios_get_bgp_api(task):
    raise NetestsFunctionNotPossible(
        "Cisco IOS does not support API..."
    )


def _ios_get_bgp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Cisco IOS does not support Netconf..."
    )


def _ios_get_bgp_ssh(task):

    outputs_dict = dict()
    output = task.run(
        name=f"{IOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=IOS_GET_BGP
    )

    if output.result != "":
        template = open(f"{TEXTFSM_PATH}cisco_ios_show_ip_bgp_summary.textfsm")
        results_template = textfsm.TextFSM(template)
        parsed_results = results_template.ParseText(output.result)
        outputs_dict["default"] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=IOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=IOS_GET_BGP_VRF.format(vrf),
            )

            if output.result != "":
                template = open(
                    f"{TEXTFSM_PATH}cisco_ios_show_ip_bgp_summary.textfsm"
                )
                results_template = textfsm.TextFSM(template)
                parsed_results = results_template.ParseText(output.result)
                outputs_dict[vrf] = parsed_results

    bgp_sessions = _ios_bgp_converter(task.host.name, outputs_dict)
    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
