#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from ncclient import manager
from xml.etree import ElementTree
from functions.workers.device import Device
from const.constants import VRF_DATA_KEY, VRF_DEFAULT_RT_LST


class DeviceNC(Device, ABC):

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
            options,
        )

    def validate_xml(self, output):
        return ElementTree.fromstring(output)

    def format_rpc_output(self, output):
        return ElementTree.tostring(output, encoding='utf8', method='xml')

    def get_no_vrf(self, task):
        if "no_key" in self.commands.get('default_vrf').keys():
            self.commands_output = self.exec_call(
                task,
                self.commands.get('default_vrf').get('no_key')
            )
        else:
            for key, command in self.commands.get('default_vrf').items():
                self.commands_output[key] = self.exec_call(task, command)

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
        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    def exec_call_get(self, task, command):
        pass

    def exec_call_get_config(self, task, command):
        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False
        ) as m:

            vrf_config = m.get_config(
                source=self.source,
                filter=(
                    'subtree',
                    (
                        command
                    )
                )
            ).data_xml
            self.validate_xml(vrf_config)
            return vrf_config
