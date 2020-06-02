#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.tools.cli import parse_textfsm
from netests.mappings import get_bgp_state_brief
from netests.constants import NOT_SET
from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)


def _ios_bgp_ssh_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if "BGP not active" not in v:
            v = parse_textfsm(
                content=v,
                template_file='cisco_ios_show_ip_bgp_summary.textfsm'
            )

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

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
