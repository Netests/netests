#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_api import DeviceAPI
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible


class IosxrAPI(DeviceAPI):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={},
    ):
        raise NetestsFunctionNotPossible(
            "Cisco IOS-XR - API - Not Possible"
        )
