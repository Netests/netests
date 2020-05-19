#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_nc import DeviceNC
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible


class CumulusNC(DeviceNC):

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
            "Cumulus - Netconf - Not Possible"
        )
