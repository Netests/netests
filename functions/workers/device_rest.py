#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from abc import ABC
from functions.workers.device import Device
from const.constants import CUMULUS_GET_VRF, VRF_DATA_KEY
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter
from exceptions.netests_exceptions import NetestsHTTPStatusCodeError


class DeviceREST(Device, ABC):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={}
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )

    def check_status_code(self, status_code):
        if status_code != 200:
            raise NetestsHTTPStatusCodeError()

    def payload_to_json(self, payload):
        return json.dumps(payload)
