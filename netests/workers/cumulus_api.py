#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from functions.workers.device_api import DeviceAPI
from const.constants import CUMULUS_API_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from functions.converters.vrf.cumulus.api.converter import _cumulus_vrf_api_converter


class CumulusAPI(DeviceAPI, ABC):

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

        res = requests.post(
            url=f"{protocol}://{task.host.hostname}:{task.host.port}/nclu/v1/rpc",
            data=self.create_payload(command),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )
        self.check_status_code(res.status_code)
        return res.content


class VRFCumulusAPI(CumulusAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_API_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
