#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.http_request import exec_http_call
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
#from functions.facts.iosxr.api.converter import _iosxr_facts_api_converter
from functions.facts.iosxr.netconf.converter import _iosxr_facts_netconf_converter
from functions.facts.iosxr.ssh.converter import _iosxr_facts_ssh_converter
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


def _iosxr_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "IOSXR-FACT NOT IMPLEMENTED"
    )


def _iosxr_get_facts_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'iosxr'}
    ) as m:
        has_capacity = False
        for c in m.server_capabilities:
            if "openconfig.net/yang/system" in c:
                has_capacity = False
            
        if has_capacity:
            output_dict = m.get(
                filter=(
                    'subtree',
                    '''
                    <system xmlns=\"http://openconfig.net/yang/system\"/>
                    '''
                )
            ).data_xml
            ElementTree.fromstring(output_dict)
        else:
            print(">>> Cisco IOS-XR device has not the capacity required")
            print(">>> Please check YANG documentation on this link :")
            print("\t * https://github.com/YangModels/yang")
            output_dict = {}

        task.host[FACTS_DATA_HOST_KEY] = _iosxr_facts_netconf_converter(
            hostname=task.host.name,
            cmd_output=output_dict,
            options=options
        )


def _iosxr_get_facts_ssh(task, options={}):
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

    output_dict[FACTS_SYS_DICT_KEY] = (output.result)

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

    output_dict[FACTS_INT_DICT_KEY] = (output.result)

    task.host[FACTS_DATA_HOST_KEY] = _iosxr_facts_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
