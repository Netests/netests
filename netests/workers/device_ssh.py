#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests import log
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

    def exec_call(self, task, command, vrf):
        enable = task.host.platform != CUMULUS_PLATEFORM_NAME

        log.debug(
            "Run nornir netmiko_send_command function : \n"
            f" - hostname={task.host.name} \n"
            f" - enable={enable} \n"
            f" - command={command} \n"
        )

        output = task.run(
            name=command,
            task=netmiko_send_command,
            command_string=command,
            enable=enable
        )

        log.debug(
            "Run nornir netmiko_send_command function : \n"
            f" - hostname={task.host.name} \n"
            f" - enable={enable} \n"
            f" - command={command} \n"
            f" ==> Output : \n"
            f"{output.result}"
        )

        return output.result
