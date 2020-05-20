#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from netests.mappings import get_bgp_state_brief
from netests.constants import NOT_SET
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_bgp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        bgp_sessions_lst = ListBGPSessions(
            list()
        )
        if not isinstance(v, dict):
            v = json.loads(v)

        if 'vrfs' in v.keys() and k in v.get('vrfs').keys():
            for n, f in v.get("vrfs", NOT_SET) \
                         .get(k, NOT_SET) \
                         .get("peers", NOT_SET) \
                         .items():
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
                    vrf_name=k,
                    as_number=v.get("vrfs", NOT_SET)
                               .get(k, NOT_SET)
                               .get('asn', NOT_SET),
                    router_id=v.get("vrfs", NOT_SET)
                               .get(k, NOT_SET)
                               .get("routerId", NOT_SET),
                    bgp_sessions=bgp_sessions_lst,
                )
            )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
