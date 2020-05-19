#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyeapi
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.constants import ARISTA_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from netests.converters.vrf.arista.api.converter import _arista_vrf_api_converter


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

    def exec_call(self, task, command):
        c = pyeapi.connect(
            transport=task.host.get('secure_api', 'https'),
            host=task.host.hostname,
            username=task.host.username,
            password=task.host.password,
            port=task.host.port
        )
        return c.execute(command)


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
