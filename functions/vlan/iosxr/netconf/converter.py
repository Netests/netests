#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import printline
from functions.verbose_mode import (
    verbose_mode
)


def _iosxr_vrf_ssh_converter(hostname: str(), cmd_output: list) -> ListVRF:
    pass
