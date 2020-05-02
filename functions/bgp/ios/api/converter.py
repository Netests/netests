#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
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


def _ios_bgp_api_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:
    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    if verbose_mode(
        user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        print(cmd_output)

    if (
        isinstance(cmd_output, dict) and
        'Cisco-IOS-XE-bgp-oper:bgp-state-data' in cmd_output.keys() and
        'address-families' in cmd_output.get(
                                        'Cisco-IOS-XE-bgp-oper:bgp-state-data')
                                        .keys() and
        'address-family' in cmd_output.get(
                                       'Cisco-IOS-XE-bgp-oper:bgp-state-data')
                                      .get('address-families')
                                      .keys()
    ):

        for v in cmd_output.get('Cisco-IOS-XE-bgp-oper:bgp-state-data') \
                           .get('address-families') \
                           .get('address-family'):
            bgp_sessions_lst = ListBGPSessions(
                list()
            )

            if (
                'bgp-neighbor-summaries' in v.keys() and
                'bgp-neighbor-summary' in v.get('bgp-neighbor-summaries')
                                           .keys()
            ):
                if isinstance(
                    v.get('bgp-neighbor-summaries')
                     .get('bgp-neighbor-summary'),
                    list
                ):
                    for n in v.get('bgp-neighbor-summaries') \
                            .get('bgp-neighbor-summary'):
                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=n.get('id', NOT_SET),
                                peer_hostname=NOT_SET,
                                remote_as=n.get('as', NOT_SET),
                                state_brief=get_bgp_state_brief(
                                    state=n.get('state', NOT_SET)
                                ),
                                session_state=n.get('state', NOT_SET),
                                state_time=n.get('up-time', NOT_SET),
                                prefix_received=n.get('prefixes-received', 0),
                                options=options
                            )
                        )

                elif isinstance(
                    v.get('bgp-neighbor-summaries')
                     .get('bgp-neighbor-summary'),
                    dict
                ):
                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=v.get('bgp-neighbor-summaries')
                                     .get('bgp-neighbor-summary')
                                     .get('id', NOT_SET),
                            peer_hostname=NOT_SET,
                            remote_as=v.get('bgp-neighbor-summaries')
                                       .get('bgp-neighbor-summary')
                                       .get('as', NOT_SET),
                            state_brief=get_bgp_state_brief(
                                state=v.get('bgp-neighbor-summaries')
                                       .get('bgp-neighbor-summary')
                                       .get('state', NOT_SET)
                            ),
                            session_state=v.get('bgp-neighbor-summaries')
                                           .get('bgp-neighbor-summary')
                                           .get('state', NOT_SET),
                            state_time=v.get('bgp-neighbor-summaries')
                                        .get('bgp-neighbor-summary')
                                        .get('up-time', NOT_SET),
                            prefix_received=v.get('bgp-neighbor-summaries')
                                             .get('bgp-neighbor-summary')
                                             .get('prefixes-received', 0),
                            options=options
                        )
                    )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                BGPSessionsVRF(
                    vrf_name=v.get('vrf-name'),
                    as_number=v.get('local-as'),
                    router_id=v.get('router-id'),
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
