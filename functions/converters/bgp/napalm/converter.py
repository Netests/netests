#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from const.constants import NOT_SET, LEVEL1
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _napalm_bgp_converter(
    hostname: str(),
    cmd_output: json,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    local_as = ""

    if "get_bgp_neighbors" in cmd_output.keys():
        for k, v in cmd_output.get("get_bgp_neighbors").items():
            bgp_sessions_lst = ListBGPSessions(list())
            for peer_ip, facts in v.get("peers").items():
                bgp_obj = BGPSession(
                    src_hostname=hostname,
                    peer_ip=peer_ip,
                    peer_hostname=facts.get("hostname", NOT_SET),
                    remote_as=facts.get("remote_as", NOT_SET),
                    state_brief=_napalm_bgp_status_converter(
                        facts.get("is_up", NOT_SET)
                    ),
                    session_state=facts.get("session_state", NOT_SET),
                    state_time=facts.get("uptime", NOT_SET),
                    prefix_received=facts.get("address_family")
                                         .get("ipv4")
                                         .get("received_prefixes"),
                )

                local_as = facts.get("local_as", NOT_SET)

                bgp_sessions_lst.bgp_sessions.append(bgp_obj)

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=_napalm_bgp_vrf_converter(k),
                as_number=local_as,
                router_id=v.get("router_id"),
                bgp_sessions=bgp_sessions_lst,
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    bgp = BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

    if verbose_mode(
        user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f'>>>>> {hostname}')
        PP.pprint(bgp.to_json())

    return bgp


def _napalm_bgp_status_converter(status: str) -> str:
    """
    This function is used to standardize BGP sessions state.
    Napalm use is_up=True and is_enable=True to simplify BGP state.
    In this project we use "UP/DOWN".

    'is_enabled': True,
    'is_up': True,

    :param status:
    :return str: Standard name of BGP state
    """
    if str(status).upper() == "TRUE":
        return "UP"
    elif str(status).upper() == "FALSE":
        return "DOWN"
    else:
        return status


def _napalm_bgp_vrf_converter(vrf_name: str) -> str:
    """
    This function is used to standardize Global routing table name (vrf_name).
    Napalm named this routing table "global".
    Other word is "global", "grt" or "default".
    In this project we use "default".

    :param vrf_name:
    :return str: Global/Default routing table name
    """

    if str(vrf_name).upper() == "GLOBAL" or str(vrf_name).upper() == "GRT":
        return "default"
    else:
        return vrf_name
