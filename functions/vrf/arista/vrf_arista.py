#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    ARISTA_GET_VRF
)
from functions.vrf.vrf_converter import (
    _arista_vrf_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _arista_get_vrf_api(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotImplemented(
        "Arista Networks API functions is not implemented..."
    )


def _arista_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Arista Networks Netconf functions is not implemented..."
    )


def _arista_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{ARISTA_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{ARISTA_GET_VRF}",
        )

        vrf_list = _arista_vrf_converter(
            task.host.name, json.loads(output.result))

        task.host[VRF_DATA_KEY] = vrf_list
