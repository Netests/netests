#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.constants import CUMULUS_GET_VRF, VRF_DATA_KEY
from netests.converters.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter


class VRFCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
