#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    CUMULUS_GET_VRF,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
# from functions.vrf.vrf_converter import (
#     _cumulus_vrf_converter
# )
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _cumulus_get_vrf_api(task):
    raise NetestsFunctionNotImplemented(
        "Cumulus Networks API functions is not implemented..."
    )


def _cumulus_get_vrf_netconf(task):
    raise NetestsFunctionNotPossible(
        "Cumulus Networks does not support Netconf..."
    )


def _cumulus_get_vrf_ssh(task):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{CUMULUS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{CUMULUS_GET_VRF}",
        )

        template = open(
            f"{TEXTFSM_PATH}cumulus_net_show_bgp_vrf.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(output.result)

        list_vrf = ListVRF(list())

        for line in parsed_results:
            vrf = VRF(
                vrf_name=line[0],
                vrf_id=line[1]
            )

            list_vrf.vrf_lst.append(vrf)

        task.host[VRF_DATA_KEY] = list_vrf
