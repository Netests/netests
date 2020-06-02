#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import pyeapi
import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.converters.bgp.arista.api import _arista_bgp_api_converter
from netests.converters.facts.arista.api import _arista_facts_api_converter
from netests.converters.lldp.arista.api import _arista_lldp_api_converter
from netests.converters.ospf.arista.api import _arista_ospf_api_converter
from netests.converters.vrf.arista.api import _arista_vrf_api_converter
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.constants import (
    VRF_DATA_KEY,
    VRF_DEFAULT_RT_LST,
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    ARISTA_API_GET_BGP,
    ARISTA_API_GET_BGP_VRF,
    ARISTA_GET_FACTS,
    ARISTA_GET_INT,
    ARISTA_GET_DOMAIN,
    ARISTA_API_GET_OSPF,
    ARISTA_API_GET_OSPF_RID,
    ARISTA_API_GET_OSPF_VRF,
    ARISTA_API_GET_OSPF_RID_VRF,
    ARISTA_GET_LLDP,
    ARISTA_GET_VRF
)


class AristaAPI(DeviceAPI, ABC):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={},
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )

    def exec_call(self, task, command, vrf):
        c = pyeapi.connect(
            transport=task.host.get('secure_api', 'https'),
            host=task.host.hostname,
            username=task.host.username,
            password=task.host.password,
            port=task.host.port
        )
        return c.execute(command)

    def exec_call_list(self, task, vrf):
        command_to_exec = list()
        if 'default_vrf' in self.commands.keys():
            for key, command in self.commands.get('default_vrf').items():
                command_to_exec.append(command)

        if 'vrf' in self.commands.keys():
            for vrf in task.host[VRF_DATA_KEY].vrf_lst:
                if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                    for key, command in self.commands.get('vrf').items():
                        command_to_exec.append(command.format(vrf.vrf_name))

        self.commands_output = self.exec_call(task, command_to_exec, vrf)

    def exec_call_without_pyeapi(self, task, command):
        """
        This function is used to avoid exception from pyeapi library.
        If OSPF is not running pyeapi will raise an error ...
        """
        p = self.use_https(task.host.get('secure_api', True))

        res = requests.post(
            url=f"{p}://{task.host.hostname}:{task.host.port}/command-api",
            data=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "method": "runCmds",
                    "params": {
                        "format": "json",
                        "timestamps": False,
                        "autoComplete": False,
                        "expandAliases": False,
                        "includeErrorDetail": False,
                        "cmds": [
                            f"{command}"
                        ],
                        "version": 1
                    },
                    "id": "EapiExplorer-1"
                }
            ),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )

        self.check_status_code(res.status_code)
        return res.content


class BGPAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_API_GET_BGP
                },
                "vrf": {
                    "no_key": ARISTA_API_GET_BGP_VRF
                }
            },
            vrf_loop=True,
            converter=_arista_bgp_api_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )

    def get_loop_vrf(self, task):
        self.exec_call_list(task, "vrf")


class CDPAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Arista doesn't support CDP"
        )


class FactsAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": ARISTA_GET_FACTS,
                    "get_infos_int": ARISTA_GET_INT,
                    "get_infos_domain": ARISTA_GET_DOMAIN,
                }
            },
            vrf_loop=False,
            converter=_arista_facts_api_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )

    def get_no_vrf(self, task):
        self.exec_call_list(task, "vrf")


class LLDPAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_arista_lldp_api_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "rid": ARISTA_API_GET_OSPF_RID,
                    "data": ARISTA_API_GET_OSPF
                },
                "vrf": {
                    "rid": ARISTA_API_GET_OSPF_RID_VRF,
                    "data": ARISTA_API_GET_OSPF_VRF
                }
            },
            vrf_loop=True,
            converter=_arista_ospf_api_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )

    def exec_call(self, task, command, vrf):
        return self.exec_call_without_pyeapi(task, command)


class VRFAristaAPI(AristaAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_arista_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
