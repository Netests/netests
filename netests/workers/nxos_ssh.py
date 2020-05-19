#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.constants import NEXUS_GET_VRF, VRF_DATA_KEY
from netests.converters.vrf.nxos.ssh.converter import _nxos_vrf_ssh_converter


class VRFNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
