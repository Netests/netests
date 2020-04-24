#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.bgp import BGP
from const.constants import NOT_SET, LEVEL4
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_bgp_netconf_converter(hostname: str(), cmd_outputs: dict) -> BGP:
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        PP.pprint(json.loads(cmd_outputs))

    raise Exception()
