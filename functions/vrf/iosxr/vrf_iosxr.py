#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    TEXTFSM_PATH,
    VRF_DATA_KEY,
    IOSXR_GET_VRF
)
from functions.vrf.vrf_converter import (
    _iosxr_vrf_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


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

        template = open(
            f"{TEXTFSM_PATH}cisco_xr_show_vrf_detail.textfsm")
        results_template = textfsm.TextFSM(template)

        # Return value
        # Example : [
        #   ['mgmt', '1', '<not set>'],
        #   ['tenant-1', '2', '10.255.255.103:103']
        # ]

        parsed_results = results_template.ParseText(output.result)
        vrf_list = _iosxr_vrf_converter(
            hostname=task.host.name,
            cmd_output=parsed_results
        )

        task.host[VRF_DATA_KEY] = vrf_list
