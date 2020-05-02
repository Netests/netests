#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xmltodict
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    BGP_SESSIONS_HOST_KEY,
    IOSXR_GET_BGP_RID,
    IOSXR_GET_BGP_PEERS,
    IOSXR_VRF_GET_BGP_RID,
    IOSXR_VRF_GET_BGP_PEERS,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible
# from functions.bgp.iosxr.api.converter import _iosxr_bgp_api_converter
from functions.bgp.iosxr.netconf.converter import _iosxr_bgp_netconf_converter
from functions.bgp.iosxr.ssh.converter import _iosxr_bgp_ssh_converter


def _iosxr_get_bgp_api(task):
    raise NetestsFunctionNotPossible(
        "Cisco IOS-XR does not support HTTP REST API..."
    )


def _iosxr_get_bgp_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False
    ) as m:

        bgp_config = m.get_config(
            source='running',
            filter=NETCONF_FILTER.format(
                "<bgp "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\""
                "/>"
            )
        ).data_xml

    ElementTree.fromstring(bgp_config)

    task.host[BGP_SESSIONS_HOST_KEY] = _iosxr_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_output=bgp_config,
        options=options
    )


def _iosxr_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{IOSXR_GET_BGP_PEERS}",
        task=netmiko_send_command,
        command_string=f"{IOSXR_GET_BGP_PEERS}",
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default'] = dict()
    output_dict['default']['peers'] = output.result

    output = task.run(
        name=f"{IOSXR_GET_BGP_RID}",
        task=netmiko_send_command,
        command_string=f"{IOSXR_GET_BGP_RID}",
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['rid'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=IOSXR_VRF_GET_BGP_PEERS.format(vrf),
                task=netmiko_send_command,
                command_string=IOSXR_VRF_GET_BGP_PEERS.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf] = dict()
            output_dict[vrf]['peers'] = output.result
            
            output = task.run(
                name=f"{IOSXR_VRF_GET_BGP_RID}",
                task=netmiko_send_command,
                command_string=IOSXR_VRF_GET_BGP_RID.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result


    task.host[BGP_SESSIONS_HOST_KEY] = _iosxr_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
