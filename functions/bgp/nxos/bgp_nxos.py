#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    BGP_SESSIONS_HOST_KEY,
    NEXUS_GET_BGP,
    NEXUS_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.bgp_converters import (
    _nexus_bgp_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _nexus_get_bgp_api(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus Network API functions is not implemented..."
    )


def _nexus_get_bgp_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus Network Netconf functions is not implemented..."
    )


def _nexus_get_bgp_ssh(task):

    outputs_lst = list()
    output = task.run(
        name=f"{NEXUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_BGP
    )

    if output.result != "":
        outputs_lst.append(json.loads(output.result))

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=NEXUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_BGP_VRF.format(vrf),
            )

            if output.result != "":
                outputs_lst.append(json.loads(output.result))

    bgp_sessions = _nexus_bgp_converter(task.host.name, outputs_lst)
    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
