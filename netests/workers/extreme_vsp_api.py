#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.converters.facts.extreme_vsp.api import (
    _extreme_vsp_facts_api_converter
)
from netests.converters.lldp.extreme_vsp.api import (
    _extreme_vsp_lldp_api_converter
)
from netests.constants import FACTS_DATA_HOST_KEY, LLDP_DATA_HOST_KEY
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible


class ExtremeVSPAPI(DeviceAPI, ABC):

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
        protocol = self.use_https(task.host.get('secure_api', True))
        login = requests.post(
            url=(
                f"{protocol}://{task.host.hostname}:{task.host.port}"
                "/auth/token/"
            ),
            headers={
                'Content-Type': 'application/json',
            },
            data="""
                {
                    "username": "%s",
                    "password": "%s"
                }
            """ % (task.host.username, task.host.password)
        )
        auth_token = json.loads(login.content).get('token')

        data = requests.get(
            url=(
                f"{protocol}://{task.host.hostname}:{task.host.port}"
                f"/rest/restconf/data/{command}"
            ),
            headers={
                'X-Auth-Token': auth_token,
            }
        )

        self.check_status_code(data.status_code)
        return data.content


class BGPExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Extreme_VSP - BGP - API - Not Possible"
        )


class CDPExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Extreme_VSP - CDP - API - Not Possible"
        )


class FactsExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": "openconfig-system:system",
                    "get_infos_int": "openconfig-interfaces:interfaces"
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_facts_api_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "openconfig-lldp:lldp/interfaces"
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_lldp_api_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Extreme_VSP - OSPF - API - Not Possible"
        )


class VRFExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Extreme_VSP - VRF - API - Not Possible"
        )
