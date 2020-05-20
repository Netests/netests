#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests.workers.device import Device
from netests.constants import VRF_DATA_KEY, VRF_DEFAULT_RT_LST
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

    def exec_call(self, task, command):
        output = task.run(
            name=command,
            task=netmiko_send_command,
            command_string=command,
        )
        self.print_nr_result(output)
        return output.result
