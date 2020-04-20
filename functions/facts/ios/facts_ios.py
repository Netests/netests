#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from xml.dom import minidom
from ncclient import manager
from xml.etree import ElementTree
from functions.http_request import exec_http_call
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.facts.ios.api.converter import _ios_facts_api_converter
from functions.facts.ios.netconf.converter import _ios_facts_netconf_converter
from functions.facts.ios.ssh.converter import _ios_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    IOS_GET_FACTS,
    IOS_GET_INT,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DATA_HOST_KEY
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _ios_get_facts_api(task, options={}):
    output_dict = exec_http_call(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="Cisco-IOS-XE-native:native",
        header={
            "Content-Type": "application/json",
            "Accept": "application/yang-data+json"
        },
        path="/restconf/data/"
    )

    task.host[FACTS_DATA_HOST_KEY] = _ios_facts_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_facts_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:

        output_dict = m.get(
            filter=NETCONF_FILTER.format(
                "<native xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\"/>"
            )
        ).data_xml

        ElementTree.fromstring(output_dict)

        task.host[FACTS_DATA_HOST_KEY] = _ios_facts_netconf_converter(
            hostname=task.host.name,
            cmd_output=output_dict,
            options=options
        )


def _ios_get_facts_ssh(task, options={}):
    output_dict = dict()

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
