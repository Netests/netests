#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_extreme_vsp
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.lldp.extreme_vsp.api.converter import (
    _extreme_vsp_lldp_api_converter
)
from functions.lldp.extreme_vsp.ssh.converter import (
    _extreme_vsp_lldp_ssh_converter
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    LLDP_DATA_HOST_KEY,
    EXTREME_VSP_GET_LLDP
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _extreme_vsp_get_lldp_api(task, options={}):
    output = exec_http_extreme_vsp(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="openconfig-lldp:lldp/interfaces",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output)

    task.host[LLDP_DATA_HOST_KEY] = _extreme_vsp_lldp_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _extreme_vsp_get_lldp_netconf(task):
    raise NetestsFunctionNotPossible("Extreme VSP - LLDP - Netconf")


def _extreme_vsp_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{EXTREME_VSP_GET_LLDP}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_LLDP,
        enable=True
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _extreme_vsp_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
