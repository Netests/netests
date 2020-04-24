#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _cumulus_bgp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:
    pass
