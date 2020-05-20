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
from netests.mappings import get_bgp_state_brief, get_bgp_peer_uptime
from netests.constants import NOT_SET, BGP_UPTIME_FORMAT_MS


def _cumulus_bgp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v, dict):
            v = json.loads(v)

        peer = False
        if (
            'ipv4 unicast' in v.keys() and
            'ipv4Unicast' in v.get('ipv4 unicast').keys() and
            'peers' in v.get('ipv4 unicast').get('ipv4Unicast').keys()
        ):
            sub_dict = v.get('ipv4 unicast').get('ipv4Unicast')
            peer = True

        elif (
            'ipv4 unicast' in v.keys() and
            'peers' in v.get('ipv4 unicast').keys()
        ):
            sub_dict = v.get('ipv4 unicast')
            peer = True

        if peer:
            bgp_vrf = BGPSessionsVRF(
                vrf_name=k,
                as_number=sub_dict.get('as', NOT_SET),
                router_id=sub_dict.get('routerId', NOT_SET),
                bgp_sessions=ListBGPSessions(
                    bgp_sessions=list()
                )
            )
            for i, p in sub_dict.get('peers').items():
                bgp_vrf.bgp_sessions.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=i,
                        peer_hostname=p.get('hostname', NOT_SET),
                        remote_as=p.get('remoteAs', NOT_SET),
                        state_brief=get_bgp_state_brief(
                            p.get('state', NOT_SET)
                        ),
                        session_state=p.get('state', NOT_SET),
                        state_time=get_bgp_peer_uptime(
                            value=p.get('peerUptimeMsec', NOT_SET),
                            format=BGP_UPTIME_FORMAT_MS
                        ),
                        prefix_received=p.get('prefixReceivedCount', NOT_SET),
                        options=options
                    )
                )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
