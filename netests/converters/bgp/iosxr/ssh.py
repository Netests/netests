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


def _iosxr_bgp_ssh_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if "BGP instance" not in v:
            v['peers'] = parse_textfsm(
                content=v.get('peers'),
                template_file='cisco_xr_show_bgp_neighbors.textfsm'
            )
            v['rid'] = parse_textfsm(
                content=v.get('rid'),
                template_file='cisco_xr_show_bgp.textfsm'
            )

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

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
