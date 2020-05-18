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
