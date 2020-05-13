#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_call_arista
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ospf.arista.api.converter import _arista_ospf_api_converter
from functions.ospf.arista.netconf.converter import (
    _arista_ospf_netconf_converter
)
from functions.ospf.arista.ssh.converter import _arista_ospf_ssh_converter
from exceptions.netests_exceptions import NetestsFunctionNotImplemented
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL4,
    OSPF_SESSIONS_HOST_KEY,
    ARISTA_GET_OSPF,
    ARISTA_GET_OSPF_RID,
    ARISTA_GET_OSPF_VRF,
    ARISTA_GET_OSPF_RID_VRF,
    ARISTA_API_GET_OSPF,
    ARISTA_API_GET_OSPF_RID,
    ARISTA_API_GET_OSPF_VRF,
    ARISTA_API_GET_OSPF_RID_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _arista_get_ospf_api(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output_dict['default']['rid'] = exec_http_call_arista(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=ARISTA_API_GET_OSPF_RID,
        secure_api=task.host.get('secure_api', 'https'),
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict['default']['rid'])

    output_dict['default']['data'] = exec_http_call_arista(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=ARISTA_API_GET_OSPF,
        secure_api=task.host.get('secure_api', 'https'),
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict['default']['data'])

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = dict()
            output_dict[vrf]['rid'] = exec_http_call_arista(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                command=ARISTA_API_GET_OSPF_RID_VRF.format(vrf),
                secure_api=task.host.get('secure_api', 'https'),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL4
            ):
                print(output_dict[vrf]['rid'])

            output_dict[vrf]['data'] = exec_http_call_arista(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                command=ARISTA_API_GET_OSPF_VRF.format(vrf),
                secure_api=task.host.get('secure_api', 'https'),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL4
            ):
                print(output_dict[vrf]['data'])

    task.host[OSPF_SESSIONS_HOST_KEY] = _arista_ospf_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _arista_get_ospf_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "Arista - OSPF - Netconf - Not Implemented"
    )
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False
    ) as m:

        vrf_config = m.get(
            filter(
                'subtree',
                '<ospfv2 "http://openconfig.net/yang/ospfv2"/>'
            )
        ).data_xml

        ElementTree.fromstring(vrf_config)

        task.host[OSPF_SESSIONS_HOST_KEY] = _arista_ospf_netconf_converter(
            hostname=task.host.name,
            cmd_output=vrf_config,
            options=options
        )


def _arista_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output = task.run(
        name=f"{ARISTA_GET_OSPF}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_OSPF,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['data'] = output.result

    output = task.run(
        name=f"{ARISTA_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_OSPF_RID,
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
                name=ARISTA_GET_OSPF_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_OSPF_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['data'] = output.result

            output = task.run(
                name=ARISTA_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=ARISTA_GET_OSPF_RID_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result

    task.host[OSPF_SESSIONS_HOST_KEY] = _arista_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
