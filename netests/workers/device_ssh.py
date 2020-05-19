#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from functions.workers.device import Device
from const.constants import VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from nornir.plugins.tasks.networking import netmiko_send_command


class DeviceSSH(Device, ABC):
    
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

    def get(self, task):
        if self.vrf_loop and "vrf" in self.commands.keys():
            self.get_loop_vrf(task)
        elif "default_vrf" in self.commands.keys():
            self.get_no_vrf(task)
        self.call_converter(task)

    def get_no_vrf(self, task):
        for key, command in self.commands.get('default_vrf').items():
            output = task.run(
                name=f"{command}",
                task=netmiko_send_command,
                command_string=command,
            )
            self.print_nr_result(output)
            self.commands_output = output.result

    def get_loop_vrf(self, task):
        output_dict = dict()
        for key, command in self.commands.get('default_vrf').items():
            output = task.run(
                name=f"{command}",
                task=netmiko_send_command,
                command_string=command,
            )
            self.print_nr_result(output)
            self.commands_output['default'][key] = output.result

        for key, command in self.commands.get('vrf').items():
            for vrf in task.host[VRF_DATA_KEY].vrf_lst:
                if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                    if vrf.vrf_name not in output_dict.keys():
                            output_dict[vrf.vrf_name] = dict()
                    output = task.run(
                        name=command.format(vrf.vrf_name),
                        task=netmiko_send_command,
                        command_string=command.format(vrf.vrf_name),
                    )
                    self.print_nr_result(output)
                    self.commands_output[vrf.vrf_name][key] = output.result
