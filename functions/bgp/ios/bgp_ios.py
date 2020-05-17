#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.bgp.ios.api.converter import _ios_bgp_api_converter
from functions.bgp.ios.netconf.converter import _ios_bgp_netconf_converter
from functions.bgp.ios.ssh.converter import _ios_bgp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    BGP_SESSIONS_HOST_KEY,
    IOS_GET_BGP,
    IOS_GET_BGP_VRF,
    VRF_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _ios_get_bgp_api(task, options={}):
    output_dict = exec_http_call(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="Cisco-IOS-XE-bgp-oper:bgp-state-data",
        secure_api=True,
        header={
            "Content-Type": "application/json",
            "Accept": "application/yang-data+json"
        },
        path="/restconf/data/"
    )

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_bgp_netconf(task, options={}):
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
                "<bgp-state-data "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-oper\""
                "/>"
            )
        ).data_xml

        ElementTree.fromstring(output_dict)

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_output=cmd_output,
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

    for vrf in task.host[VRF_DATA_KEY].vrf_lst:
        if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=IOS_GET_BGP_VRF.format(vrf.vrf_name),
                task=netmiko_send_command,
                command_string=IOS_GET_BGP_VRF.format(vrf.vrf_name),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if output.result != "":
                output_dict[vrf.vrf_name] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _ios_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
