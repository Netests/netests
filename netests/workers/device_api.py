#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from abc import ABC, abstractmethod
from netests.workers.device import Device
from netests.exceptions.netests_exceptions import NetestsHTTPStatusCodeError


class DeviceAPI(Device, ABC):

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

    @abstractmethod
    def exec_call(self, task, command, vrf):
        pass

    def check_status_code(self, status_code):
        if status_code != 200:
            raise NetestsHTTPStatusCodeError()

    def payload_to_json(self, payload):
        return json.dumps(payload)

    def use_https(self, secure_api):
        return "https" if secure_api else "http"
