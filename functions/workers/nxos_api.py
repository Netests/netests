#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from functions.workers.device_api import DeviceAPI
from const.constants import NEXUS_API_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from functions.converters.vrf.nxos.api.converter import _nxos_vrf_api_converter


class NxosAPI(DeviceAPI, ABC):

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

        res = requests.post(
            url=f"{protocol}://{task.host.hostname}:{task.host.port}/ins",
            headers={
                'Content-Type': 'application/json',
            },
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False,
            data="""{
                "ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": "%s",
                    "output_format": "json"
                }
            }""" % (str(command))
        )
        self.check_status_code(res.status_code)
        return res.content


class VRFNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_API_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
