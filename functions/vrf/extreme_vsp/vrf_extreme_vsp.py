#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    TEXTFSM_PATH,
    VRF_DATA_KEY,
    EXTREME_VSP_GET_VRF
)
from functions.vrf.vrf_converter import (
    _extreme_vsp_vrf_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _extreme_vsp_get_vrf_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Extreme Networks API functions is not supported..."
    )


def _extreme_vsp_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Extreme Networks Netconf functions is not implemented..."
    )


def _extreme_vsp_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{EXTREME_VSP_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{EXTREME_VSP_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_vrf.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)

        vrf_list = _extreme_vsp_vrf_converter(task.host.name, parsed_results)

        task.host[VRF_DATA_KEY] = vrf_list
