#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    EXTREME_VSP_GET_VRF
)
from functions.vrf.extreme_vsp.ssh.converter import (
    _extreme_vsp_vrf_ssh_converter
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _extreme_vsp_get_vrf_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Extreme Networks VRF is not supported with Restconf ..."
    )


def _extreme_vsp_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Extreme Networks API functions is not supported..."
    )


def _extreme_vsp_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{EXTREME_VSP_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{EXTREME_VSP_GET_VRF}",
        )

        task.host[VRF_DATA_KEY] = _extreme_vsp_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )
