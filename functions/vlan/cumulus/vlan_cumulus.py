#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import textfsm
import requests
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL3,
    TEXTFSM_PATH,
    BOND_DATA_LIST_KEY,
    VLAN_DATA_HOST_KEY,
    VLAN_VRF_LIST_KEY,
    VLAN_VRF_DETAIL_KEY,
    VLAN_VRF_MEMBERS_KEY,
    CUMULUS_GET_VLAN,
    CUMULUS_API_GET_VLAN,
    CUMULUS_GET_VLAN_VRF,
    CUMULUS_GET_VLAN_MEM
)
from functions.global_tools import printline
from functions.vlan.cumulus.ssh.converter import (
    _cumulus_vlan_ssh_converter
)
from functions.vlan.cumulus.api.converter import (
    _cumulus_vlan_api_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _cumulus_get_vlan_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Cumulus Networks API functions is not implemented..."
    )


def _cumulus_get_vlan_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Cumulus Networks does not support Netconf..."
    )


def _cumulus_get_vlan_ssh(task, filters={}, level=None, own_vars={}):
    outputs_dict = dict()

    output = task.run(
        name=f"{CUMULUS_GET_VLAN_VRF}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN_VRF
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
            print(output.result)

    if output.result != "":
        template = open(
            f"{TEXTFSM_PATH}cumulus_net_show_vrf_list.textfsm"
        )
        results_template = textfsm.TextFSM(template)
        parsed_results = results_template.ParseText(output.result)
        outputs_dict[VLAN_VRF_LIST_KEY] = parsed_results

    output = task.run(
        name=f"{CUMULUS_GET_VLAN}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        print(output.result)

    if output.result != "":
        outputs_dict[VLAN_VRF_DETAIL_KEY] = json.loads(output.result)

    output = task.run(
        name=f"{CUMULUS_GET_VLAN_MEM}",
        task=netmiko_send_command,
        command_string=CUMULUS_GET_VLAN_MEM
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        print(output.result)

    if output.result != "":
        outputs_dict[VLAN_VRF_MEMBERS_KEY] = json.loads(output.result)

    if filters is not None and filters.get("get_bond", True):
        bond_lst = task.host[BOND_DATA_LIST_KEY]
    else:
        bond_lst = list()

    vlans = _cumulus_vlan_ssh_converter(
        hostname=task.host.name,
        cmd_output=outputs_dict,
        filters=filters,
        bond_lst=bond_lst,
    )

    task.host[VLAN_DATA_HOST_KEY] = vlans
