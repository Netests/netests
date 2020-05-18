#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyeapi
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.lldp.arista.api.converter import _arista_lldp_api_converter
from functions.lldp.arista.ssh.converter import _arista_lldp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    ARISTA_GET_LLDP,
    LLDP_DATA_HOST_KEY
)


def _arista_get_lldp_api(task, options={}):
    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )
    output = c.execute([ARISTA_GET_LLDP])

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print(output)

    task.host[LLDP_DATA_HOST_KEY] = _arista_lldp_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _arista_get_lldp_netconf(task):
    pass


def _arista_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{ARISTA_GET_LLDP}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_LLDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _arista_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
