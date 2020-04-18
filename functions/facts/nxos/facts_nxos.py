#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from ncclient import manager
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_nxos
from functions.facts.nxos.api.converter import _nxos_facts_api_converter
from functions.facts.nxos.ssh.converter import _nxos_facts_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NEXUS_GET_FACTS,
    NEXUS_API_GET_FACTS,
    NEXUS_GET_INT,
    NEXUS_API_GET_INT,
    NEXUS_GET_DOMAIN,
    NEXUS_API_GET_DOMAIN,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DATA_HOST_KEY,
    FACTS_DOMAIN_DICT_KEY
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _nxos_get_facts_api(task, options={}):
    output_dict = dict()

    output_dict[FACTS_SYS_DICT_KEY] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_FACTS,
        secure_api=task.host.get('secure_api', True)
    )

    output_dict[FACTS_INT_DICT_KEY] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_INT,
        secure_api=task.host.get('secure_api', True)
    )

    output_dict[FACTS_DOMAIN_DICT_KEY] = exec_http_nxos(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        command=NEXUS_API_GET_DOMAIN,
        secure_api=task.host.get('secure_api', True)
    )

    task.host[FACTS_DATA_HOST_KEY] = _nxos_facts_api_converter(
        hostname=task.host.hostname,
        cmd_output=output_dict,
        options=options
    )


def _nxos_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "NX-OS Facts is not implemented with Netconf ..."
    )
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False
    ) as m:

        output_dict = m.get(
            filter=(
                'subtree',
                '''
                <show xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
                    <version/>
                </show>
                '''
            )
        ).data_xml

        print(output_dict)


def _nxos_get_facts_ssh(task, options={}):
    output_dict = dict()
    output = task.run(
        name=f"{NEXUS_GET_FACTS}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_FACTS
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_SYS_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{NEXUS_GET_INT}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_INT
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_INT_DICT_KEY] = (json.loads(output.result))

    output = task.run(
        name=f"{NEXUS_GET_DOMAIN}",
        task=netmiko_send_command,
        command_string=NEXUS_GET_DOMAIN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "":
        output_dict[FACTS_DOMAIN_DICT_KEY] = (json.loads(output.result))

    task.host[FACTS_DATA_HOST_KEY] = _nxos_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
