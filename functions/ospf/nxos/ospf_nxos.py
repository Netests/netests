#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from jnpr.junos import Device
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_nxos
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ospf.nxos.api.converter import _nxos_ospf_api_converter
from functions.ospf.nxos.ssh.converter import _nxos_ospf_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    OSPF_SESSIONS_HOST_KEY,
    NEXUS_GET_OSPF,
    NEXUS_GET_OSPF_RID,
    NEXUS_GET_OSPF_VRF,
    NEXUS_GET_OSPF_RID_VRF,
    NEXUS_API_GET_OSPF,
    NEXUS_API_GET_OSPF_VRF,
    NEXUS_API_GET_OSPF_RID,
    NEXUS_API_GET_OSPF_RID_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _nxos_get_ospf_api(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output_dict['default']['data'] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_OSPF,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict['default']['data'])

    output_dict['default']['rid'] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_OSPF_RID,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict['default']['rid'])

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = dict()
            output_dict[vrf]['data'] = exec_http_nxos(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                command=NEXUS_API_GET_OSPF_VRF.format(vrf),
                secure_api=task.host.get('secure_api', True)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print(output_dict[vrf]['data'])

            output_dict[vrf]['rid'] = exec_http_nxos(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                command=NEXUS_API_GET_OSPF_RID_VRF.format(vrf),
                secure_api=task.host.get('secure_api', True)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print(output_dict[vrf]['rid'])

    task.host[OSPF_SESSIONS_HOST_KEY] = _nxos_ospf_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _nxos_get_ospf_netconf(task):
    pass


def _nxos_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output = task.run(
        name=f"{NEXUS_GET_OSPF}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_OSPF,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['data'] = output.result

    output = task.run(
        name=f"{NEXUS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_OSPF_RID,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['rid'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = dict()
            output = task.run(
                name=NEXUS_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_OSPF_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['data'] = output.result

            output = task.run(
                name=NEXUS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=NEXUS_GET_OSPF_RID_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result

    task.host[OSPF_SESSIONS_HOST_KEY] = _nxos_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
