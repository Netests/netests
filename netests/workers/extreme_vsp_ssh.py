#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.workers.device_ssh import DeviceSSH
from const.constants import EXTREME_VSP_GET_VRF, VRF_DATA_KEY
from functions.converters.vrf.extreme_vsp.ssh.converter import _extreme_vsp_vrf_ssh_converter


class VRFExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": EXTREME_VSP_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
