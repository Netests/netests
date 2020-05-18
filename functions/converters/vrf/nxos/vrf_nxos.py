#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call
from functions.http_request import exec_http_nxos
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.vrf.nxos.api.converter import _nxos_vrf_api_converter
from functions.vrf.nxos.ssh.converter import _nxos_vrf_ssh_converter
from functions.vrf.nxos.netconf.converter import _nxos_vrf_netconf_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    VRF_DATA_KEY,
    NEXUS_GET_VRF,
    NEXUS_API_GET_VRF
)


def _nxos_get_vrf_api(task, options={}):
    vrf_config = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_VRF,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(vrf_config)

    task.host[VRF_DATA_KEY] = _nxos_vrf_api_converter(
        hostname=task.host.name,
        cmd_output=vrf_config,
        options=options
    )


def _nxos_get_vrf_resconf(task, options={}):
    vrf_config = exec_http_call(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="data/Cisco-NX-OS-device:System/inst-items"
    )

    ElementTree.fromstring(vrf_config)

    task.host[VRF_DATA_KEY] = _nxos_vrf_api_converter(
        hostname=task.host.name,
        cmd_output=vrf_config,
        options=options
    )


def _nxos_get_vrf_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'nexus'}
    ) as m:

        vrf_config = m.get_config(
            source='running',
            filter=(
                'subtree',
                '''
                <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
                    <inst-items/>
                </System>
                '''
            )
        ).data_xml

        ElementTree.fromstring(vrf_config)

        task.host[VRF_DATA_KEY] = _nxos_vrf_netconf_converter(
            hostname=task.host.name,
            cmd_output=vrf_config,
            options=options
        )


def _nxos_get_vrf_ssh(task, options={}):
    output = task.run(
        name=f"{NEXUS_GET_VRF}",
        task=netmiko_send_command,
        command_string=f"{NEXUS_GET_VRF}",
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[VRF_DATA_KEY] = _nxos_vrf_ssh_converter(
        hostname=task.host.name,
        cmd_output=json.loads(output.result),
        options=options
    )
