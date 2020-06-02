#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.protocols.bgp import BGP
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    BGP_ALL_BGP_UP_KEY,
    BGP_STATE_BRIEF_DOWN
)


def _compare_transit_bgp_up(task, options={}):
    task.host[BGP_ALL_BGP_UP_KEY] = _compare_bgp_up(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        bgp_host_data=task.host.get(BGP_SESSIONS_HOST_KEY, None),
        test=False,
        options=options,
        task=task
    )

    return task.host[BGP_ALL_BGP_UP_KEY]


def _compare_bgp_up(
    host_keys,
    hostname,
    groups,
    bgp_host_data: BGP,
    test=False,
    options={},
    task=Task
):
    log.debug(
        "BGP_SESSIONS_HOST_KEY in host_keys="
        f"{BGP_SESSIONS_HOST_KEY in host_keys}\n"
    )
    result = True
    if BGP_SESSIONS_HOST_KEY in host_keys:
        for vrf in bgp_host_data.bgp_sessions_vrf_lst.bgp_sessions_vrf:
            for i in vrf.bgp_sessions.bgp_sessions:
                if i.state_brief == BGP_STATE_BRIEF_DOWN:
                    result = False

    return result
