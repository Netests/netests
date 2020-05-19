#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.constants import CUMULUS_API_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from netests.converters.vrf.cumulus.api.converter import _cumulus_vrf_api_converter
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

    def create_payload(self, command):
        return self.payload_to_json(
            {
                "cmd": f"{command}"
            }
        )

    def exec_call(self, task, command):
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


class VRFExtremeVSPAPI(ExtremeVSPAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Extreme_VSP - VRF - API - Not Possible"
        )
