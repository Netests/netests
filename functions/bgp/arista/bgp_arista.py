#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyeapi
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.bgp.arista.api.converter import _arista_bgp_api_converter
from functions.bgp.arista.ssh.converter import _arista_bgp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    BGP_SESSIONS_HOST_KEY,
    ARISTA_GET_BGP,
    ARISTA_API_GET_BGP,
    ARISTA_GET_BGP_VRF,
    ARISTA_API_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _arista_get_bgp_api(task, options={}):
    commands_to_execute = [ARISTA_API_GET_BGP]
    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            commands_to_execute.append(ARISTA_API_GET_BGP_VRF.format(vrf))

    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )
    output = c.execute(commands_to_execute)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print(output)

    task.host[BGP_SESSIONS_HOST_KEY] = _arista_bgp_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _arista_get_bgp_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Arista Networks Netconf functions is not implemented..."
    )


def _arista_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{ARISTA_GET_BGP}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_BGP,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=ARISTA_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _arista_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
