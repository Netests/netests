#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotImplemented


import os
import textfsm
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from functions.facts.ios.api.converter import _ios_facts_api_converter
from functions.facts.ios.netconf.converter import _ios_facts_netconf_converter
from functions.facts.ios.ssh.converter import _ios_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    TEXTFSM_PATH,
    IOS_GET_FACTS,
    IOS_GET_INT,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DATA_HOST_KEY
)


def _ios_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "IOS-FACT NOT IMPLEMENTED"
    )


def _ios_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "IOS-FACT NOT IMPLEMENTED"
    )


def _ios_get_facts_ssh(task, options={}):
    outputs_dict = dict()

    output = task.run(
        name=f"{IOS_GET_FACTS}",
        task=netmiko_send_command,
        command_string=IOS_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
            print_result(output)

    outputs_dict[FACTS_SYS_DICT_KEY] = (output.result)

    output = task.run(
        name=f"{IOS_GET_INT}",
        task=netmiko_send_command,
        command_string=IOS_GET_INT
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
            print_result(output)

    outputs_dict[FACTS_INT_DICT_KEY] = (output.result)

    task.host[FACTS_DATA_HOST_KEY] = _ios_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=outputs_dict,
        options=options
    )
