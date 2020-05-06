#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_nxos
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.cdp.nxos.api.converter import _nxos_cdp_api_converter
from functions.cdp.nxos.netconf.converter import _nxos_cdp_netconf_converter
from functions.cdp.nxos.ssh.converter import _nxos_cdp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NEXUS_GET_CDP,
    NEXUS_API_GET_CDP,
    CDP_DATA_HOST_KEY
)


def _nxos_get_cdp_api(task, options={}):
    cdp_config = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_CDP,
        secure_api=task.host.get('secure_api', True)
    )

    task.host[CDP_DATA_HOST_KEY] = _nxos_cdp_api_converter(
        hostname=task.host.name,
        cmd_output=cdp_config,
        options=options
    )


def _nxos_get_cdp_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'nexus'}
    ) as m:

        cdp_config = dict()

        ElementTree.fromstring(cdp_config)

        task.host[CDP_DATA_HOST_KEY] = _nxos_cdp_netconf_converter(
            hostname=task.host.name,
            cmd_output=cdp_config,
            options=options
        )


def _nxos_get_cdp_ssh(task, options={}):
    output = task.run(
        name=f"{NEXUS_GET_CDP}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_CDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[CDP_DATA_HOST_KEY] = _nxos_cdp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result
    )
