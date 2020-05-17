#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from const.constants import VRF_DATA_KEY
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter


class CumulusSSH():

    command: str
    results: list
    options: dict

    def __init__(self, command, options):
        self.command = command
        self.options = options
        self.results = list()


    def get(self, task):
        output = task.run(
            name=f"{self.command}",
            task=netmiko_send_command,
            command_string=f"{self.command}",
        )
        self.results.append(output)

        task.host[VRF_DATA_KEY] = _cumulus_vrf_ssh_converter(
            hostname=task.host.name,
            cmd_output=output.result,
            options=self.optionsoptions
        )
