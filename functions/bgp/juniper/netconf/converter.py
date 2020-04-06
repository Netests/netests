#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.bgp import (
    LEVEL5,
    BGP
)
from functions.global_tools import (
    printline
)
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_bgp_netconf_converter(hostname: str(), cmd_outputs: dict) -> BGP:
    if verbose_mode(
        user_value=os.environ["NETESTS_VERBOSE"],
        needed_value=LEVEL5
    ):
        printline()
        PP.pprint(
            json.loads(cmd_outputs).get("data")
                                   .get("configuration")
                                   .get("protocols")
                                   .get("bgp")
        )

    raise Exception()
