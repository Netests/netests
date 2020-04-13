#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pyeapi
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import VRF_DATA_KEY, ARISTA_GET_VRF
from functions.vrf.arista.ssh.converter import _arista_vrf_ssh_converter
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _arista_get_vrf_api(task, options={}):
    c =  pyeapi.connect(
        transport="http",
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )
    eapi = pyeapi.client.Node(c)
    output = eapi.run_commands(['show vrf'])
    print(output['result'])


def _arista_get_vrf_netconf(task, options={}):
    raise NetestsFunctionNotPossible(
        "Arista Networks Netconf functions is not implemented..."
    )


def _arista_get_vrf_ssh(task, options={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{ARISTA_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{ARISTA_GET_VRF}",
        )

        task.host[VRF_DATA_KEY] = _arista_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=json.loads(output.result),
            options=options
        )
