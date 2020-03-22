#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    BGP_SESSIONS_HOST_KEY,
    CUMULUS_GET_BGP,
    CUMULUS_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.bgp_converters import (
    _cumulus_bgp_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _cumulus_get_bgp_api(task):
    raise NetestsFunctionNotImplemented(
        "Cumulus Network API functions is not implemented..."
    )


def _cumulus_get_bgp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Cumulus Network does not support Netconf..."
    )


def _cumulus_get_bgp_ssh(task):

    outputs_lst = list()
    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP,
    )

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=CUMULUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_BGP_VRF.format(vrf),
            )

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    task.host[BGP_SESSIONS_HOST_KEY] = _cumulus_bgp_converter(
        hostname=task.host.name,
        cmd_outputs=outputs_lst
    )
