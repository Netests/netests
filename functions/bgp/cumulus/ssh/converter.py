#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief, get_bgp_peer_uptime
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    BGP_UPTIME_FORMAT_MS
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _cumulus_bgp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        PP.pprint(cmd_output)

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        peer = False
        if (
            'ipv4 unicast' in v.keys() and 
            isinstance(v.get('ipv4 unicast'), dict) and
            'ipv4Unicast' in v.get('ipv4 unicast').keys() and
            'peers' in v.get('ipv4 unicast').get('ipv4Unicast').keys()
        ):
            sub_dict = v.get('ipv4 unicast').get('ipv4Unicast')
            peer = True

        elif (
            'ipv4 unicast' in v.keys() and
            isinstance(v.get('ipv4 unicast'), dict) and
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

    bgp = BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(bgp.to_json())

    return bgp
