#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.constants import JUNOS_GET_VRF_DETAIL, VRF_DATA_KEY
from netests.converters.vrf.juniper.ssh.converter import _juniper_vrf_ssh_converter


class VRFJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": JUNOS_GET_VRF_DETAIL
                }
            },
            vrf_loop=False,
            converter=_juniper_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
