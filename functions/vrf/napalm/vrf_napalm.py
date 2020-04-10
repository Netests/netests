#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.plugins.tasks.networking import napalm_get
from const.constants import VRF_DATA_KEY
from functions.vrf.vrf_converter import (
    _napalm_vrf_converter
)


def _generic_vrf_napalm(task, filters={}, level=None, own_vars={}):
    print(f"Start _generic_napalm_vrf with {task.host.name} ")

    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_network_instances"]
    )
    # print(output.result)

    if output.result != "":
        vrf_list = _napalm_vrf_converter(
            hostname=task.host.name,
            cmd_output=output.result
        )

        task.host[VRF_DATA_KEY] = vrf_list
