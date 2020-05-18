#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from functions.workers.device_rest import DeviceREST
from const.constants import CUMULUS_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter


class CumulusREST(DeviceREST, ABC):

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

    def exec_call(self, task, command):
        if task.host.get('secure_api', True):
            protocol = "https"
        else:
            protocol = "http"

        res = requests.post(
            url=f"{protocol}://{task.host.name}:{task.host.port}/nclu/v1/rpc",
            data=self.create_payload(command),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.username}"
            ),
            verify=False
        )
        self.check_status_code(res.status_code)
        return res.content
