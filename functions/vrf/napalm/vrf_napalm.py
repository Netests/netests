#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL2, VRF_DATA_KEY
from functions.vrf.napalm.converter import _napalm_vrf_converter


def _generic_vrf_napalm(task, options={}):
    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_network_instances"]
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
            printline()
            print_result(output)

    if output.result != "":
        task.host[VRF_DATA_KEY] = _napalm_vrf_converter(
            hostname=task.host.name,
            cmd_output=output.result,
            options=options
        )
