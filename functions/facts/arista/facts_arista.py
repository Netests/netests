#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyeapi
from ncclient import manager
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.facts.arista.api.converter import _arista_facts_api_converter
from functions.facts.arista.netconf.converter import (
    _arista_facts_netconf_converter
)
from functions.facts.arista.ssh.converter import _arista_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    ARISTA_GET_FACTS,
    FACTS_SYS_DICT_KEY,
    ARISTA_GET_INT,
    FACTS_INT_DICT_KEY,
    ARISTA_GET_DOMAIN,
    FACTS_DOMAIN_DICT_KEY,
    FACTS_DATA_HOST_KEY,
    NETCONF_FILTER
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _arista_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented("Arista - Facts - Netconf")
    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )
    output = c.execute([
        ARISTA_GET_FACTS,
        ARISTA_GET_INT,
        ARISTA_GET_DOMAIN
    ])

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print(output)

    task.host[FACTS_DATA_HOST_KEY] = _arista_facts_api_converter(
        hostname=task.host.name,
        cmd_output=output,
        options=options
    )


def _arista_get_facts_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
    ) as m:

        output_dict = m.get(
            filter=NETCONF_FILTER.format(
                "<native "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\""
                "/>"
            )
        ).data_xml

        ElementTree.fromstring(output_dict)

        task.host[FACTS_DATA_HOST_KEY] = _arista_facts_netconf_converter(
            hostname=task.host.name,
            cmd_output=output_dict,
            options=options
        )


def _arista_get_facts_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{ARISTA_GET_FACTS}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict[FACTS_SYS_DICT_KEY] = output.result

    output = task.run(
        name=f"{ARISTA_GET_INT}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_INT
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict[FACTS_INT_DICT_KEY] = output.result

    output = task.run(
        name=f"{ARISTA_GET_DOMAIN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_DOMAIN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict[FACTS_DOMAIN_DICT_KEY] = output.result

    task.host[FACTS_DATA_HOST_KEY] = _arista_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
