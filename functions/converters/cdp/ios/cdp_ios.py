#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from ncclient import manager
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_call
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.cdp.ios.api.converter import _ios_cdp_api_converter
from functions.cdp.ios.netconf.converter import _ios_cdp_netconf_converter
from functions.cdp.ios.ssh.converter import _ios_cdp_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    NETCONF_FILTER,
    IOS_GET_CDP,
    CDP_DATA_HOST_KEY
)


def _ios_get_cdp_api(task, options={}):
    output_dict = exec_http_call(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="Cisco-IOS-XE-cdp-oper:cdp-neighbor-details",
        secure_api=True,
        header={
            "Content-Type": "application/json",
            "Accept": "application/yang-data+json"
        },
        path="/restconf/data/"
    )

    task.host[CDP_DATA_HOST_KEY] = _ios_cdp_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _ios_get_cdp_netconf(task, options={}):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False,
        device_params={'name': 'iosxe'}
    ) as m:

        cmd_output = output_dict = m.get(
            filter=NETCONF_FILTER.format(
                "<cdp-neighbor-details "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper\""
                "/>"
            )
        ).data_xml

        ElementTree.fromstring(output_dict)

    task.host[CDP_DATA_HOST_KEY] = _ios_cdp_netconf_converter(
        hostname=task.host.name,
        cmd_output=cmd_output,
        options=options
    )


def _ios_get_cdp_ssh(task, options={}):
    output = task.run(
        name=f"{IOS_GET_CDP}",
        task=netmiko_send_command,
        command_string=IOS_GET_CDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[CDP_DATA_HOST_KEY] = _ios_cdp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result
    )
