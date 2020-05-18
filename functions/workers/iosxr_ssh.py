#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.workers.device_ssh import DeviceSSH
from const.constants import IOSXR_GET_VRF, VRF_DATA_KEY
from functions.converters.vrf.iosxr.ssh.converter import _iosxr_vrf_ssh_converter


class VRFIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOSXR_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_iosxr_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
