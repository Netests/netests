#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_nxos
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.bgp.nxos.api.converter import _nxos_bgp_api_converter
from functions.bgp.nxos.ssh.converter import _nxos_bgp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    BGP_SESSIONS_HOST_KEY,
    NEXUS_GET_BGP,
    NEXUS_API_GET_BGP,
    NEXUS_GET_BGP_VRF,
    NEXUS_API_GET_BGP_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _nexus_get_bgp_api(task, options={}):
    output_dict = dict()
    output_dict['default'] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_BGP,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict['default'])

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = exec_http_nxos(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                command=NEXUS_API_GET_BGP_VRF.format(vrf),
                secure_api=task.host.get('secure_api', True)
            )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL2
        ):
            print(output_dict[vrf])

    task.host[BGP_SESSIONS_HOST_KEY] = _nxos_bgp_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _nexus_get_bgp_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus Network Netconf functions is not implemented..."
    )


def _nexus_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{NEXUS_GET_BGP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_BGP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict['default'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=NEXUS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if output.result != "":
                output_dict[vrf] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _nxos_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
