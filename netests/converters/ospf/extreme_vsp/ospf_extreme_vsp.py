#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ospf.extreme_vsp.ssh.converter import (
    _extreme_vsp_ospf_ssh_converter
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    OSPF_SESSIONS_HOST_KEY,
    EXTREME_VSP_GET_OSPF,
    EXTREME_VSP_GET_OSPF_RID,
    EXTREME_VSP_GET_OSPF_INTERFACES,
    EXTREME_VSP_GET_OSPF_VRF,
    EXTREME_VSP_GET_OSPF_RID_VRF,
    EXTREME_VSP_GET_OSPF_INTERFACES_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _extreme_vsp_get_ospf_api(task, options={}):
    pass


def _extreme_vsp_get_ospf_netconf(task):
    pass


def _extreme_vsp_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['data'] = output.result

    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_RID,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['rid'] = output.result

    output = task.run(
        name=f"{EXTREME_VSP_GET_OSPF_INTERFACES}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_OSPF_INTERFACES,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['int'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = dict()
            output = task.run(
                name=EXTREME_VSP_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['data'] = output.result

            output = task.run(
                name=EXTREME_VSP_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_RID_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result

            output = task.run(
                name=EXTREME_VSP_GET_OSPF_INTERFACES_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=EXTREME_VSP_GET_OSPF_INTERFACES_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['int'] = output.result

    task.host[OSPF_SESSIONS_HOST_KEY] = _extreme_vsp_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
