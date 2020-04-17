#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import json
from jnpr.junos import Device
from xml.etree import ElementTree
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call_juniper
from functions.facts.juniper.api.converter import _juniper_facts_api_converter
from functions.facts.juniper.netconf.converter import (
    _juniper_facts_netconf_converter
)
from functions.facts.juniper.ssh.converter import _juniper_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_DATA_HOST_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_SERIAL_DICT_KEY,
    FACTS_CONFIG_DICT_KEY,
    FACTS_MEMORY_DICT_KEY,
    JUNOS_GET_FACTS,
    JUNOS_GET_INT,
    JUNOS_GET_MEMORY,
    JUNOS_GET_CONFIG_SYSTEM,
    JUNOS_GET_SERIAL
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _juniper_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "Juniper - Facts with API doesn't work due to malformed HTTP body"
    )

    cmd_output = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint=[
            "get-interface-information?terse=",
            "get-chassis-inventory?detail=",
            "get-software-information",
            "get-system-memory-information",
        ],
        secure_api=task.host.get('secure_api', False)
    )

    ElementTree.fromstring(cmd_output)

    task.host[FACTS_DATA_HOST_KEY] = _juniper_facts_api_converter(
        hostname=task.host.name,
        cmd_output=cmd_output,
        options=options
    )


def _juniper_get_facts_netconf(task, options={}):
    d = Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    )

    d.open()
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = d.facts
    cmd_output[FACTS_INT_DICT_KEY] = d.rpc.get_interface_information(
        terse=True)

    task.host[FACTS_DATA_HOST_KEY] = _juniper_facts_netconf_converter(
        hostname=task.host.hostname,
        cmd_output=cmd_output,
        options=options
    )
    d.close()


def _juniper_get_facts_ssh(task, options={}):
    outputs_dict = dict()

    output = task.run(
        name=f"{JUNOS_GET_FACTS}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        outputs_dict[FACTS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_INT}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_INT
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        outputs_dict[FACTS_INT_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_MEMORY}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_MEMORY
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        outputs_dict[FACTS_MEMORY_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_CONFIG_SYSTEM}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_CONFIG_SYSTEM
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        outputs_dict[FACTS_CONFIG_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{JUNOS_GET_SERIAL}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_SERIAL
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        outputs_dict[FACTS_SERIAL_DICT_KEY] = (json.loads(output.result))

    task.host[FACTS_DATA_HOST_KEY] = _juniper_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=outputs_dict,
        options=options
    )
