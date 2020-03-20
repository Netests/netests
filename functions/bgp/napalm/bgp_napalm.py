#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.plugins.tasks.networking import napalm_get
from const.constants import BGP_SESSIONS_HOST_KEY
from functions.bgp.bgp_converters import (
    _napalm_bgp_converter
)


def _generic_bgp_napalm(task):

    print(f"Start _generic_bgp_napalm with {task.host.name} ")
    output = task.run(
        name=f"NAPALM get_bgp_neighbors {task.host.platform}",
        task=napalm_get,
        getters=["get_bgp_neighbors"],
    )

    if output.result != "":
        bgp_sessions = _napalm_bgp_converter(task.host.name, output.result)
        task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
