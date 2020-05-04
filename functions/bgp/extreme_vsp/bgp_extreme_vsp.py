#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.bgp.extreme_vsp.ssh.converter import (
    _extreme_vsp_bgp_ssh_converter
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    BGP_SESSIONS_HOST_KEY,
    EXTREME_VSP_GET_BGP,
    EXTREME_VSP_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
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


def _extreme_vsp_get_bgp_ssh(task, options={}):
    outputs_dict = dict()
    output = task.run(
        name=f"{EXTREME_VSP_GET_BGP}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_BGP,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output.result)

    if (
        output.result != "" and
        "BGP instance does not exist for VRF" not in output.result
    ):
        outputs_dict["default"] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=EXTREME_VSP_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print(output.result)

            if (
                output.result != "" and
                "BGP instance does not exist for VRF" not in output.result
            ):
                outputs_dict[vrf] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _extreme_vsp_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=outputs_dict,
        options=options
    )
