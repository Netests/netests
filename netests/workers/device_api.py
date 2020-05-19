#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from abc import ABC, abstractmethod
from netests.workers.device import Device
from netests.constants import VRF_DATA_KEY, VRF_DEFAULT_RT_LST
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
    def exec_call(self, task, command):
        pass

    def check_status_code(self, status_code):
        if status_code != 200:
            raise NetestsHTTPStatusCodeError()

    def payload_to_json(self, payload):
        return json.dumps(payload)

    def use_https(self, secure_api):
        return "https" if secure_api else "http"

    def get_no_vrf(self, task):
        for key, command in self.commands.get('default_vrf').items():
            self.commands_output = self.exec_call(task, command)

    def get_loop_vrf(self, task):
        output_dict = dict()
        if 'default_vrf' in self.commands.keys():
            output_dict['default'] = dict()
            for key, command in self.commands.get('default_vrf').items():
                output_dict['default'][key] = self.exec_call(task, command)

        if 'vrf' in self.commands.keys():
            for key, command in self.commands.get('vrf').items():
                for vrf in task.host[VRF_DATA_KEY].vrf_lst:
                    if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                        if vrf.vrf_name not in output_dict.keys():
                            output_dict[vrf.vrf_name] = dict()
                        output_dict[vrf.vrf_name][key] = self.exec_call(
                            task,
                            command
                        )
