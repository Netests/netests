#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.workers.device_ssh import DeviceSSH
from const.constants import IOS_GET_VRF, VRF_DATA_KEY
from functions.converters.vrf.ios.ssh.converter import _ios_vrf_ssh_converter


class VRFIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_ios_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
