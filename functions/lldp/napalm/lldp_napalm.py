#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from functions.lldp.napalm.converter import _napalm_lldp_converter
from const.constants import NOT_SET, LEVEL2, LLDP_DATA_HOST_KEY

def _generic_lldp_napalm(task, options={}):
    output = task.run(
        name=f"NAPALM get_lldp_neighbors_detail {task.host.platform}",
        task=napalm_get,
        getters=["get_lldp_neighbors_detail"]
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[LLDP_DATA_HOST_KEY] = _napalm_lldp_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
