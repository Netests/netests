#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from netests.constants import NOT_SET
from nornir.plugins.functions.text import print_result
from netests.converters.ping.retrieve_ping import retrieve_ping_from_yaml
from netests.converters.ping.ping_generate import _generic_generate_ping_cmd


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

    data = devices.run(
        task=_generic_generate_ping_cmd,
        on_failed=True,
        num_workers=10
    )
