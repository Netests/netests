#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    IOSXR_GET_VRF
)
from functions.vrf.iosxr.ssh.converter import _iosxr_vrf_ssh_converter
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _iosxr_get_vrf_api(task):
    raise NetestsFunctionNotImplemented(
        "Cisco IOSXR API functions is not implemented...."
    )


def _iosxr_get_vrf_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco IOSXR Netconf functions is not implemented..."
    )


def _iosxr_get_vrf_ssh(task):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{IOSXR_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{IOSXR_GET_VRF}",
        )

        vrf_list = _iosxr_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )

        task.host[VRF_DATA_KEY] = vrf_list
