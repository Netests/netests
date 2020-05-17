#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call
from nornir.plugins.functions.text import print_result
from functions.ospf.ios.api.converter import _ios_ospf_api_converter
from functions.ospf.ios.netconf.converter import _ios_ospf_netconf_converter
from functions.ospf.ios.ssh.converter import _ios_ospf_ssh_converter
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    OSPF_SESSIONS_HOST_KEY,
    IOS_GET_OSPF,
    IOS_GET_OSPF_NEI,
    IOS_GET_OSPF_INT,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _ios_get_ospf_api(task, options={}):
    output_dict = exec_http_call(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="Cisco-IOS-XE-ospf-oper:ospf-oper-data",
        secure_api=True,
        header={
            "Content-Type": "application/json",
            "Accept": "application/yang-data+json"
        },
        path="/restconf/data/"
    )

    task.host[OSPF_SESSIONS_HOST_KEY] = _ios_ospf_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_ospf_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:

        cmd_output = output_dict = m.get(
            filter=NETCONF_FILTER.format(
                "<ospf-oper-data "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper\""
                "/>"
            )
        ).data_xml

        ElementTree.fromstring(output_dict)

    task.host[OSPF_SESSIONS_HOST_KEY] = _ios_ospf_netconf_converter(
        hostname=task.host.name,
        cmd_output=cmd_output,
        options=options
    )


def _ios_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{IOS_GET_OSPF_NEI}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF_NEI,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['data'] = output.result

    output = task.run(
        name=f"{IOS_GET_OSPF}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['rid'] = output.result

    output = task.run(
        name=f"{IOS_GET_OSPF_INT}",
        task=netmiko_send_command,
        command_string=IOS_GET_OSPF_INT,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['int'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            pass

    task.host[OSPF_SESSIONS_HOST_KEY] = _ios_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
