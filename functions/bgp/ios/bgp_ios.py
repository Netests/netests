#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.bgp.ios.api.converter import _ios_bgp_api_converter
from functions.bgp.ios.netconf.converter import _ios_bgp_netconf_converter
from functions.bgp.ios.ssh.converter import _ios_bgp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    BGP_SESSIONS_HOST_KEY,
    IOS_GET_BGP,
    IOS_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _ios_get_bgp_api(task, options={}):
    output_dict = dict()

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_bgp_netconf(task, options={}):
    output_dict = dict()

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{IOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=IOS_GET_BGP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict["default"] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=IOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=IOS_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if output.result != "":
                output_dict[vrf] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
