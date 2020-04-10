#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.vlan.arista.api.converter import _arista_vlan_api_converter
from functions.vlan.arista.ssh.converter import _arista_vlan_ssh_converter
from functions.vlan.arista.netconf.converter import (
    _arista_vlan_netconf_converter
)
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL2,
    ARISTA_GET_VLAN,
    ARISTA_GET_IP_VLAN,
    ARISTA_GET_INT_VLAN
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _arista_get_vlan_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Arista Networks API functions is not implemented..."
    )


def _arista_get_vlan_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Arista Networks Netconf functions is not implemented..."
    )


def _arista_get_vlan_ssh(task, filters={}, level=None, own_vars={}):
    outputs_dict = dict()

    output_get = task.run(
        name=f"{ARISTA_GET_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_VLAN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_get.result)

    output_get_ip = task.run(
        name=f"{ARISTA_GET_IP_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_IP_VLAN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_get_ip.result)

    output_get_int = task.run(
        name=f"{ARISTA_GET_INT_VLAN}",
        task=netmiko_send_command,
        command_string=ARISTA_GET_INT_VLAN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_get_int.result)

    if output_get.result != "" and output_get_ip.result != "" and output_get_int.result != "":
        outputs_dict[VLAN_GET_L2] = json.loads(output_get.result)
        outputs_dict[VLAN_GET_L3] = json.loads(output_get_ip.result)
        outputs_dict[VLAN_GET_INT] = json.loads(output_get_int.result)

    task.host[VLAN_DATA_HOST_KEY] = _arista_vlan_ssh_converter(
        cmd_output=outputs_dict,
        filters=filters,
        level=level,
        own_vars=own_vars
    )
