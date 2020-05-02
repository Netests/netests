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


def _iosxr_bgp_ssh_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:
    
    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        v['peers'] = parse_textfsm(
            content=v.get('peers'),
            template_file='cisco_xr_show_bgp_neighbors.textfsm'
        )
        v['rid'] = parse_textfsm(
            content=v.get('rid'),
            template_file='cisco_xr_show_bgp.textfsm'
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
        asn = NOT_SET
        if len(v['peers']) > 0:
            for i in v['peers']:
                asn = i[3]
                bgp_sessions_lst.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=i[0],
                        peer_hostname=NOT_SET,
                        remote_as=i[2],
                        state_brief=get_bgp_state_brief(
                            i[4]
                        ),
                        session_state=i[4],
                        state_time=NOT_SET,
                        prefix_received=NOT_SET,
                    )
                )

            if len(v['rid']) > 0:
                rid = v['rid'][0][0]
            else:
                rid = NOT_SET

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
