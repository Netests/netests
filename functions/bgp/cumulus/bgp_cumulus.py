#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    BGP_SESSIONS_HOST_KEY,
    CUMULUS_GET_BGP,
    CUMULUS_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.verbose_mode import verbose_mode
# from functions.bgp.cumulus.api.converter import _cumulus_bgp_api_converter
from functions.bgp.cumulus.ssh.converter import _cumulus_bgp_ssh_converter
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


def _cumulus_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{CUMULUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_BGP,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict['default'] = json.loads(output.result)

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=CUMULUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=CUMULUS_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if output.result != "":
                output_dict[vrf] = json.loads(output.result)

    task.host[BGP_SESSIONS_HOST_KEY] = _cumulus_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
