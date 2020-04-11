#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    IOS_GET_VRF
)
from functions.vrf.ios.ssh.converter import _ios_vrf_ssh_converter
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _ios_get_vrf_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Cisco IOS API functions is not supported..."
    )


def _ios_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Cisco IOS Netconf functions is not implemented..."
    )


def _ios_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{IOS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{IOS_GET_VRF}",
        )

        task.host[VRF_DATA_KEY] = _ios_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )
