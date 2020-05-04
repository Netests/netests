#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core import Nornir
from functions.bgp.bgp_gets import get_bgp
from const.constants import (
    BGP_ALL_BGP_UP_KEY,
    BGP_SESSIONS_HOST_KEY,
    BGP_STATE_BRIEF_DOWN,
)


ERROR_HEADER = "Error import [bgp_checks.py]"
HEADER_GET = "[netests - bgp_checks]"


def get_bgp_up(nr: Nornir, filters={}, level=None, vars={}):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_bgp(nr)

    devices.run(
        task=check_if_all_bgp_sessions_are_up,
        on_failed=True,
        num_workers=10
    )

    return_value = True

    for device in devices.inventory.hosts:
        if devices.inventory.hosts[device].get(BGP_ALL_BGP_UP_KEY) is False:
            return_value = False

    return return_value


def check_if_all_bgp_sessions_are_up(task):

    all_are_up = True

    for bgp_session_vrf in task.host.get(
        BGP_SESSIONS_HOST_KEY
    ).bgp_sessions_vrf_lst.bgp_sessions_vrf:
        for bgp_session in bgp_session_vrf.bgp_sessions.bgp_sessions:
            if bgp_session.state_brief == BGP_STATE_BRIEF_DOWN:
                all_are_up = False

    task.host[BGP_ALL_BGP_UP_KEY] = all_are_up
