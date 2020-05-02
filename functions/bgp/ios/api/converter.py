#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL1, LEVEL3
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_bgp_api_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:
    pass
