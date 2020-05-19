#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_call_cumulus
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.lldp.cumulus.api.converter import _cumulus_lldp_api_converter
from functions.lldp.cumulus.ssh.converter import _cumulus_lldp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    CUMULUS_GET_LLDP_CDP,
    CUMULUS_API_GET_LLDP_CDP,
    LLDP_DATA_HOST_KEY
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _cumulus_get_lldp_api(task, options={}):
    output = exec_http_call_cumulus(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        cumulus_cmd=CUMULUS_API_GET_LLDP_CDP,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output)

    task.host[LLDP_DATA_HOST_KEY] = _cumulus_lldp_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _cumulus_get_lldp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Cumulus Network does not support Netconf..."
    )


def _cumulus_get_lldp_ssh(task, options={}):
    output = task.run(
        name=f"{CUMULUS_GET_LLDP_CDP}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_LLDP_CDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _cumulus_lldp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
