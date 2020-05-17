#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import VRF_DATA_KEY
from functions.workers.cumulus_ssh import CumulusSSH
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter


class CumulusSSHBGP(cumulusSSH):

    command: str
    results: list
    options: dict

    def __init__(self, command, options):
        super().__init__(command, options)

    def get(self, task):
        super().get()
