#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call_cumulus
from functions.facts.cumulus.api.converter import _cumulus_facts_api_converter
# from functions.facts.cumulus.netconf.converter import (
# _cumulus_facts_netconf_converter
# )
from functions.facts.cumulus.ssh.converter import _cumulus_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_DATA_HOST_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    CUMULUS_GET_FACTS,
    CUMULUS_API_GET_FACTS,
    CUMULUS_GET_INT,
    CUMULUS_API_GET_INT
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _cumulus_get_facts_api(task, options={}):
    output_dict = dict()

    output_dict[FACTS_SYS_DICT_KEY] = exec_http_call_cumulus(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        cumulus_cmd=CUMULUS_API_GET_FACTS,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_SYS_DICT_KEY])

    output_dict[FACTS_INT_DICT_KEY] = exec_http_call_cumulus(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        cumulus_cmd=CUMULUS_API_GET_INT,
        secure_api=task.host.get('secure_api', True)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_INT_DICT_KEY])

    task.host[FACTS_DATA_HOST_KEY] = _cumulus_facts_api_converter(
        hostname=task.host.hostname,
        cmd_output=output_dict,
        options=options
    )


def _cumulus_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotPossible(
        "Cumulus devices don't support Netconf ..."
    )


def _cumulus_get_facts_ssh(task, options={}):
    output_dict = dict()

    output = task.run(
        name=f"{CUMULUS_GET_FACTS}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{CUMULUS_GET_INT}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_INT
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_INT_DICT_KEY] = (json.loads(output.result))

    task.host[FACTS_DATA_HOST_KEY] = _cumulus_facts_ssh_converter(
        hostname=task.host.hostname,
        cmd_output=output_dict,
        options=options
    )
