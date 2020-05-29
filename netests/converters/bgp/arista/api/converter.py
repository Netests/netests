#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from netests.mappings import get_bgp_state_brief
from netests.constants import NOT_SET


def _arista_bgp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )
    for vrf in cmd_output.get('result', []):
        if 'vrfs' in vrf.keys() and len(vrf.get('vrfs').keys()) > 0:
            bgp_sessions_lst = ListBGPSessions(
                list()
            )
            for name, facts in vrf.get("vrfs", NOT_SET).items():
                for n, f in facts.get('peers').items():
                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=n,
                            peer_hostname=f.get("hostname", NOT_SET),
                            remote_as=f.get("asn", NOT_SET),
                            state_brief=get_bgp_state_brief(
                                state=f.get('peerState')
                            ),
                            session_state=f.get("peerState", NOT_SET),
                            state_time=f.get("upDownTime", NOT_SET),
                            prefix_received=f.get("prefixReceived", NOT_SET),
                        )
                    )

                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                    BGPSessionsVRF(
                        vrf_name=name,
                        as_number=facts.get('asn', NOT_SET),
                        router_id=facts.get("routerId", NOT_SET),
                        bgp_sessions=bgp_sessions_lst,
                    )
                )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
