#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    VRF_DATA_KEY,
    IOSXR_GET_VRF
)
from functions.vrf.iosxr.netconf.converter import _iosxr_vrf_netconf_converter
from functions.vrf.iosxr.ssh.converter import _iosxr_vrf_ssh_converter
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _iosxr_get_vrf_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "Cisco IOSXR API functions is not implemented...."
    )


def _iosxr_get_vrf_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'iosxr'}
    ) as m:

        vrf_config = m.get_config(
            source='running',
            filter=NETCONF_FILTER.format(
                "<vrfs "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-infra-rsi-cfg\""
                "/>"
            )
        ).data_xml

        bgp_config = m.get_config(
            source='running',
            filter=NETCONF_FILTER.format(
                "<bgp "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\""
                "/>"
            )
        ).data_xml

    ElementTree.fromstring(vrf_config)
    ElementTree.fromstring(bgp_config)

    config = dict()
    config['BGP'] = bgp_config
    config['VRF'] = vrf_config

    task.host[VRF_DATA_KEY] = _iosxr_vrf_netconf_converter(
        hostname=task.host.name,
        cmd_output=config,
        options=options
    )


def _iosxr_get_vrf_ssh(task, options={}):
    output = task.run(
        name=f"{IOSXR_GET_VRF}",
        task=netmiko_send_command,
        command_string=f"{IOSXR_GET_VRF}",
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[VRF_DATA_KEY] = _iosxr_vrf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
