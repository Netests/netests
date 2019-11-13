#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [bgp_checks.py]"
HEADER_GET = "[netests - bgp_checks]"

########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.bgp import BGPSession, ListBGPSessions, BGPSessionsVRF, ListBGPSessionsVRF, BGP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bgp")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.bgp.bgp_gets import get_bgp
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.bgp")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from nornir.core import Nornir
    # To use advanced filters
    from nornir.core.filter import F
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def get_bgp_up(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_bgp(nr)

    data = devices.run(
        task=check_if_all_bgp_sessions_are_up,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

    return_value = True

    for device in devices.inventory.hosts:
        if devices.inventory.hosts[device].get(BGP_ALL_BGP_UP_KEY) is False:
            return_value = False

    return return_value

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic function
#
def check_if_all_bgp_sessions_are_up(task):

    all_are_up = True

    for bgp_session_vrf in task.host.get(BGP_SESSIONS_HOST_KEY).bgp_sessions_vrf_lst.bgp_sessions_vrf:
            for bgp_session in bgp_session_vrf.bgp_sessions.bgp_sessions:
                if bgp_session.state_brief == BGP_STATE_BRIEF_DOWN:
                    all_are_up = False

                    #print(f"{HEADER_GET}[{task.host.name}] The following BGP sessions is DOWN :( ...")
                    #print(f"{bgp_session}")

    task.host[BGP_ALL_BGP_UP_KEY] = all_are_up




