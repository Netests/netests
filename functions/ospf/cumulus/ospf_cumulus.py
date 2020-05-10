#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ospf.cumulus.api.converter import _cumulus_ospf_api_converter
from functions.ospf.cumulus.ssh.converter import _cumulus_ospf_ssh_converter
from exceptions.netests_exceptions import NetestsFunctionNotPossible
from const.constants import (
    NOT_SET,
    LEVEL2,
    OSPF_SESSIONS_HOST_KEY,
    CUMULUS_GET_OSPF,
    CUMULUS_GET_OSPF_RID,
    CUMULUS_GET_OSPF_VRF,
    CUMULUS_GET_OSPF_RID_VRF,
    VRF_NAME_DATA_KEY
)


def _cumulus_get_ospf_api(task, options={}):
    output_dict = dict()

    task.host[OSPF_SESSIONS_HOST_KEY] = _cumulus_ospf_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _cumulus_get_ospf_netconf(task):
    raise NetestsFunctionNotPossible(
        "Cumulus Network does not support Netconf..."
    )


def _cumulus_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output = task.run(
        name=f"{CUMULUS_GET_OSPF}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_OSPF,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['data'] = output.result

    output = task.run(
        name=f"{CUMULUS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_OSPF_RID,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['rid'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf != "default" and vrf != "global":
            output_dict[vrf] = dict()
            output = task.run(
                name=CUMULUS_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_OSPF_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['data'] = output.result

            output = task.run(
                name=CUMULUS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_OSPF_RID_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result

    task.host[OSPF_SESSIONS_HOST_KEY] = _cumulus_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
