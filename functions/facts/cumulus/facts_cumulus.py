#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from jnpr.junos import Device
from xml.etree import ElementTree
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from functions.http_request import exec_http_call_juniper
#from functions.facts.cumulus.api.converter import _cumulus_facts_api_converter
#from functions.facts.cumulus.netconf.converter import _cumulus_facts_netconf_converter
from functions.facts.cumulus.ssh.converter import _cumulus_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_DATA_HOST_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    CUMULUS_GET_FACTS,
    CUMULUS_GET_INT,
)
from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _cumulus_get_facts_api(task, options={}):
    pass


def _cumulus_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotPossible(
        "Cumulus devices don't support Netconf ..."
    )


def _cumulus_get_facts_ssh(task, options={}):
    outputs_dict = dict()

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
        outputs_dict[FACTS_SYS_DICT_KEY] = (json.loads(output.result))

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
        outputs_dict[FACTS_INT_DICT_KEY] = (json.loads(output.result))

    task.host[FACTS_DATA_HOST_KEY] = _cumulus_facts_ssh_converter(
        hostname=task.host.hostname,
        cmd_output=outputs_dict,
        options=options
    )

