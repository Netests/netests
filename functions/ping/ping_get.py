#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.core.filter import F
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.ping.retrieve_ping import retrieve_ping_from_yaml
from functions.ping.ping_generate import _generic_generate_ping_cmd
from const.constants import NOT_SET, LEVEL4


HEADER = "[netests - execute_ping]"


def get_ping(nr: Nornir, options={}) -> bool:
    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=retrieve_ping_from_yaml,
        on_failed=True,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        print_result(data)

    data = devices.run(
        task=_generic_generate_ping_cmd,
        on_failed=True,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        print_result(data)
