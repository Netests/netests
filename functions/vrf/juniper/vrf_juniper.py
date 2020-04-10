#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from jnpr.junos import Device
from xml.etree import ElementTree
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    VRF_DATA_KEY,
    JUNOS_GET_VRF_DETAIL
)
from functions.vrf.juniper.netconf.converter import (
    _juniper_vrf_netconf_converter
)
from functions.vrf.juniper.ssh.converter import (
    _juniper_vrf_ssh_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_get_vrf_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks API functions is not implemented..."
    )


def _juniper_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:

        vrf_config = m.rpc.get_instance_information(detail=True)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(ElementTree.tostring(vrf_config))

    ElementTree.fromstring(ElementTree.tostring(vrf_config))

    task.host[VRF_DATA_KEY] = _juniper_vrf_netconf_converter(
        hostname=task.host.name,
        cmd_output=vrf_config
    )


def _juniper_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        data = task.run(
            name=f"{JUNOS_GET_VRF_DETAIL}",
            task=netmiko_send_command,
            command_string=f"{JUNOS_GET_VRF_DETAIL}",
        )

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL2
        ):
            printline()
            print_result(data)

        task.host[VRF_DATA_KEY] = _juniper_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=json.loads(data.result)
        )
