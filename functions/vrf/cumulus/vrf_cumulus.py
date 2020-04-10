#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from nornir.plugins.tasks.networking import netmiko_send_command
from nornir.plugins.functions.text import print_result
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL3,
    VRF_DATA_KEY,
    CUMULUS_GET_VRF,
    CUMULUS_API_GET_VRF
)
from functions.global_tools import printline
from functions.vrf.cumulus.ssh.converter import (
    _cumulus_vrf_ssh_converter
)
from functions.vrf.cumulus.api.converter import (
    _cumulus_vrf_api_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsHTTPStatusCodeError
)


def _cumulus_get_vrf_api(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        res = requests.post(
            url=f"https://{task.host.hostname}:{task.host.port}/nclu/v1/rpc",
            data=json.dumps(
                {
                    "cmd": f"{CUMULUS_API_GET_VRF}"
                }),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL3
        ):
            print(type(res.status_code), res.status_code)
            print(type(res.content), res.content)

        if res.status_code != 200:
            raise NetestsHTTPStatusCodeError()

        task.host[VRF_DATA_KEY] = _cumulus_vrf_api_converter(
            hostname=task.host.name,
            cmd_output=res.content
        )


def _cumulus_get_vrf_netconf(task, filters={}, level=None, own_vars={}):
    raise NetestsFunctionNotPossible(
        "Cumulus Networks does not support Netconf..."
    )


def _cumulus_get_vrf_ssh(task, filters={}, level=None, own_vars={}):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{CUMULUS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{CUMULUS_GET_VRF}",
        )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL2
        ):
            printline()
            print_result(output)

        task.host[VRF_DATA_KEY] = _cumulus_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )

        
