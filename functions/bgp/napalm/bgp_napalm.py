#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from const.constants import NOT_SET, LEVEL2, BGP_SESSIONS_HOST_KEY
from functions.bgp.napalm.converter import _napalm_bgp_converter


def _generic_bgp_napalm(task, options={}):
    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_bgp_neighbors"],
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print_result(output)

    task.host[BGP_SESSIONS_HOST_KEY] = _napalm_bgp_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
