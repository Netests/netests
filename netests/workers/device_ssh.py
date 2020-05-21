#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests.workers.device import Device
from netests.constants import CUMULUS_PLATEFORM_NAME
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
        enable = task.host.platform != CUMULUS_PLATEFORM_NAME

        output = task.run(
            name=command,
            task=netmiko_send_command,
            command_string=command,
            enable=enable
        )
        self.print_nr_result(output)
        return output.result
