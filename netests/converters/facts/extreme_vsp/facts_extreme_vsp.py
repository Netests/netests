#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_extreme_vsp
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.facts.extreme_vsp.ssh.converter import (
    _extreme_vsp_facts_ssh_converter
)
from functions.facts.extreme_vsp.api.converter import (
    _extreme_vsp_facts_api_converter
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DATA_HOST_KEY,
    FACTS_DOMAIN_DICT_KEY,
    EXTREME_VSP_GET_FACTS,
    EXTREME_VSP_GET_INT,
    EXTREME_VSP_GET_DOMAIN
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _extreme_vsp_get_facts_api(task, options={}):
    output_dict = dict()
    output_dict[FACTS_SYS_DICT_KEY] = exec_http_extreme_vsp(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="openconfig-system:system",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_SYS_DICT_KEY])

    output_dict[FACTS_INT_DICT_KEY] = exec_http_extreme_vsp(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="openconfig-interfaces:interfaces",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_INT_DICT_KEY])

    task.host[FACTS_DATA_HOST_KEY] = _extreme_vsp_facts_api_converter(
        hostname=task.host.hostname,
        cmd_output=output_dict,
        options=options
    )


def _extreme_vsp_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "EXTREME_VSP-FACT NOT IMPLEMENTED"
    )


def _extreme_vsp_get_facts_ssh(task, options={}):
    output_dict = dict()

    output = task.run(
        name=f"{EXTREME_VSP_GET_FACTS}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_SYS_DICT_KEY] = (output.result)

    output = task.run(
        name=f"{EXTREME_VSP_GET_DOMAIN}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_DOMAIN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_DOMAIN_DICT_KEY] = (output.result)

    output = task.run(
        name=f"{EXTREME_VSP_GET_INT}",
        task=netmiko_send_command,
        command_string=EXTREME_VSP_GET_INT,
        enable=True
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_INT_DICT_KEY] = (output.result)

    task.host[FACTS_DATA_HOST_KEY] = _extreme_vsp_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
