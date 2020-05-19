#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from functions.workers.device_api import DeviceAPI
from const.constants import VRF_DATA_KEY
from functions.converters.vrf.juniper.api.converter import _juniper_vrf_api_converter


class JuniperAPI(DeviceAPI, ABC):

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

    def exec_call(self, task, command):
        protocol = self.use_https(task.host.get('secure_api', True))

        res = requests.get(
            url=(
                f"{protocol}://{task.host.hostname}:{task.host.port}"
                f"/rpc/{command}"
            ),
            headers={'content-type': 'application/xml'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )
        self.check_status_code(res.status_code)
        return res.content


class VRFJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get-instance-information?detail="
                }
            },
            vrf_loop=False,
            converter=_juniper_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
