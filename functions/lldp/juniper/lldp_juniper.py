#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from jnpr.junos import Device
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_call_juniper
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    JUNOS_GET_LLDP,
    LLDP_DATA_HOST_KEY
)
from functions.lldp.juniper.api.converter import _juniper_lldp_api_converter
from functions.lldp.juniper.netconf.converter import (
    _juniper_lldp_netconf_converter
)
from functions.lldp.juniper.ssh.converter import _juniper_lldp_ssh_converter



def _juniper_get_lldp_api(task, options={}):
    lldp_config = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="get-lldp-neighbors-information",
        secure_api=task.host.get('secure_api', False)
    )

    ElementTree.fromstring(lldp_config)

    task.host[LLDP_DATA_HOST_KEY] = _juniper_lldp_api_converter(
        hostname=task.host.name,
        cmd_output=lldp_config,
        options=options
    )


def _juniper_get_lldp_netconf(task, options={}):
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:
        lldp_config = m.rpc.get_lldp_neighbors_information()

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(ElementTree.tostring(lldp_config))

    ElementTree.fromstring(ElementTree.tostring(lldp_config))

    task.host[LLDP_DATA_HOST_KEY] = _juniper_lldp_netconf_converter(
        hostname=task.host.name,
        cmd_output=lldp_config,
        options=options
    )


def _juniper_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{JUNOS_GET_LLDP}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_LLDP,
        enable=True
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _juniper_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
