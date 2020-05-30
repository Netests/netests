#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core import Nornir
from netests.converters.ping.retrieve_ping import retrieve_ping_from_yaml
from netests.converters.ping.ping_generate import _generic_generate_ping_cmd


HEADER = "[netests - execute_ping]"


def get_ping(nr: Nornir, options={}) -> bool:
    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    devices.run(
        task=retrieve_ping_from_yaml,
        on_failed=True,
        num_workers=10
    )

    devices.run(
        task=_generic_generate_ping_cmd,
        on_failed=True,
        num_workers=10
    )
