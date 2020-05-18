#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from const.constants import NOT_SET, LEVEL1, LEVEL3
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_bgp_ssh_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        v = parse_textfsm(
            content=v,
            template_file='cisco_ios_show_ip_bgp_summary.textfsm'
        )
        if verbose_mode(
            user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
            needed_value=LEVEL3
        ):
            printline()
            print(v)

        bgp_sessions_lst = ListBGPSessions(
            list()
        )

        for i in v:
            asn = i[1]
            rid = i[0]

            bgp_sessions_lst.bgp_sessions.append(
                BGPSession(
                    src_hostname=hostname,
                    peer_ip=i[2],
                    peer_hostname=NOT_SET,
                    remote_as=i[3],
                    state_brief=get_bgp_state_brief(
                        i[5]
                    ),
                    session_state=i[5],
                    state_time=i[4],
                    prefix_received=NOT_SET,
                )
            )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
            BGPSessionsVRF(
                vrf_name=k,
                as_number=asn,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst,
            )
        )

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
