#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.lldp.iosxr.netconf.converter import (
    _iosxr_lldp_netconf_converter
)
from functions.lldp.iosxr.ssh.converter import _iosxr_lldp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    IOSXR_GET_LLDP,
    LLDP_DATA_HOST_KEY
)


def _iosxr_get_lldp_api(task, options={}):
    pass


def _iosxr_get_lldp_netconf(task, options={}):
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
                "<lldp "
                "xmlns="
                "\"http://cisco.com/ns/yang/Cisco-IOS-XR-ethernet-lldp-oper\""
                "/>"
            )
        ).data_xml

    ElementTree.fromstring(bgp_config)

    task.host[LLDP_DATA_HOST_KEY] = _iosxr_lldp_netconf_converter(
        hostname=task.host.name,
        cmd_output=bgp_config,
        options=options
    )


def _iosxr_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{IOSXR_GET_LLDP}",
        task=netmiko_send_command,
        command_string=IOSXR_GET_LLDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _iosxr_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
