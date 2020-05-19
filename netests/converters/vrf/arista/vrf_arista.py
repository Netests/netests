#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyeapi
from ncclient import manager
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import NOT_SET, LEVEL2, VRF_DATA_KEY, ARISTA_GET_VRF
from functions.vrf.arista.api.converter import _arista_vrf_api_converter
from functions.vrf.arista.netconf.converter import (
    _arista_vrf_netconf_converter
)
from functions.vrf.arista.ssh.converter import _arista_vrf_ssh_converter


def _arista_get_vrf_api(task, options={}):
    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )
    output = c.execute(['show vrf'])

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print(output)

    task.host[VRF_DATA_KEY] = _arista_vrf_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _arista_get_vrf_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False
    ) as m:

        vrf_config = m.get_config(
            source='running',
            filter=(
                'subtree',
                (
                    "<network-instances "
                    "xmlns=\"http://openconfig.net/yang/network-instance\""
                    "/>"
                )
            )
        ).data_xml

        ElementTree.fromstring(vrf_config)

        task.host[VRF_DATA_KEY] = _arista_vrf_netconf_converter(
            hostname=task.host.name,
            cmd_output=vrf_config,
            options=options
        )


def _arista_get_vrf_ssh(task, options={}):
    output = task.run(
        name=f"{ARISTA_GET_VRF}",
        task=netmiko_send_command,
        command_string=f"{ARISTA_GET_VRF}",
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print_result(output)

    task.host[VRF_DATA_KEY] = _arista_vrf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
