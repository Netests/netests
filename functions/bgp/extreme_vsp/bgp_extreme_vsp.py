#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    TEXTFSM_PATH,
    BGP_SESSIONS_HOST_KEY,
    EXTREME_VSP_GET_BGP,
    EXTREME_VSP_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.bgp_converters import (
    _extreme_vsp_bgp_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible
)


def _extreme_vsp_get_bgp_api(task):
    raise NetestsFunctionNotPossible(
        "Extreme Networks API functions is not implemented..."
    )


def _extreme_vsp_get_bgp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Extreme Networks Netconf functions is not implemented..."
    )


def _extreme_vsp_get_bgp_ssh(task):

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
        outputs_dict["default"] = parsed_results

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():

        if vrf not in VRF_DEFAULT_RT_LST:

            output = task.run(
                name=EXTREME_VSP_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_BGP_VRF.format(vrf),
            )

            if (
                output.result != ""
                and "BGP instance does not exist for" not in output.result
            ):
                template = open(
                    f"{TEXTFSM_PATH}extreme_vsp_show_ip_bgp_summary.textfsm"
                )
                results_template = textfsm.TextFSM(template)
                parsed_results = results_template.ParseText(output.result)
                outputs_dict[vrf] = parsed_results

    bgp_sessions = _extreme_vsp_bgp_converter(task.host.name, outputs_dict)
    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
