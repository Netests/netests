#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [bgp_compare.py]"
HEADER_GET = "[netests - compare_bgp]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from protocols.bgp import BGPSession, ListBGPSessions, BGPSessionsVRF, ListBGPSessionsVRF, BGP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bgp")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
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
def compare_bgp(nr, bgp_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare,
        bgp_data=bgp_data,
        on_failed=True,
        num_workers=10
    )
    # print_result(data.result)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(f"{HEADER_GET} Task '_compare' has failed for {value.host} (value.result={value.result}).")
            return_value = False

    return (not data.failed and return_value)

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare(task, bgp_data:json):

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    if BGP_SESSIONS_HOST_KEY in task.host.keys():

        for vrf_name, facts in bgp_data.get(task.host.name, NOT_SET).items():

            bgp_sessions_lst = ListBGPSessions(list())

            for neighbor in facts.get('neighbors', NOT_SET):
                bgp_session = BGPSession(
                    src_hostname=task.host.name,
                    peer_ip=neighbor.get('peer_ip', NOT_SET),
                    peer_hostname=neighbor.get('peer_hostname', NOT_SET),
                    remote_as=neighbor.get('remote_as', NOT_SET),
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

            bgp_session_vrf = BGPSessionsVRF(
                as_number=facts.get('asn', NOT_SET),
                router_id=facts.get('router_id', NOT_SET),
                bgp_sessions=bgp_sessions_lst
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)


        verity_bgp = BGP(
            hostname=task.host.name,
            bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
        )

        is_same = verity_bgp == task.host[BGP_SESSIONS_HOST_KEY]

        task.host[BGP_WORKS_KEY] = is_same
        return is_same

    else:
        print(f"Key {BGP_SESSIONS_HOST_KEY} is missing for {task.host.name}")
