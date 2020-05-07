#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_nxos
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.lldp.nxos.api.converter import _nxos_lldp_api_converter
from functions.lldp.nxos.netconf.converter import _nxos_lldp_netconf_converter
from functions.lldp.nxos.ssh.converter import _nxos_lldp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NEXUS_GET_LLDP,
    NEXUS_API_GET_LLDP,
    LLDP_DATA_HOST_KEY
)


def _nxos_get_lldp_api(task, options={}):
    lldp_config = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_LLDP,
        secure_api=task.host.get('secure_api', True)
    )

    task.host[LLDP_DATA_HOST_KEY] = _nxos_lldp_api_converter(
        hostname=task.host.name,
        cmd_output=lldp_config,
        options=options
    )


def _nxos_get_lldp_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'nexus'}
    ) as m:

        m.server_capabilities

        lldp_config = dict()

        ElementTree.fromstring(lldp_config)

        task.host[LLDP_DATA_HOST_KEY] = _nxos_lldp_netconf_converter(
            hostname=task.host.name,
            cmd_output=lldp_config,
            options=options
        )


def _nxos_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{NEXUS_GET_LLDP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_LLDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _nxos_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result
    )
