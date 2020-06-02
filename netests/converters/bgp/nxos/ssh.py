#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.mappings import get_bgp_state_brief
from netests.constants import NOT_SET
from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)


def _nxos_bgp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if v != "":
            if not isinstance(v, dict):
                v = json.loads(v)

            bgp_sessions_lst = ListBGPSessions(
                list()
            )

            if (
                'TABLE_vrf' in v.keys() and
                'ROW_vrf' in v.get('TABLE_vrf').keys() and
                'TABLE_neighbor' in v.get('TABLE_vrf')
                                     .get('ROW_vrf')
                                     .keys() and
                'ROW_neighbor' in v.get('TABLE_vrf')
                                   .get('ROW_vrf')
                                   .get('TABLE_neighbor')
                                   .keys()
            ):
                if isinstance(
                    v.get("TABLE_vrf")
                    .get("ROW_vrf")
                    .get("TABLE_neighbor")
                    .get("ROW_neighbor", NOT_SET),
                    list,
                ):
                    for n in v.get("TABLE_vrf", NOT_SET) \
                              .get("ROW_vrf", NOT_SET) \
                              .get("TABLE_neighbor", NOT_SET) \
                              .get("ROW_neighbor", NOT_SET):

                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=n.get("neighbor-id", NOT_SET),
                                peer_hostname=n.get("interfaces", NOT_SET),
                                remote_as=n.get("remoteas", NOT_SET),
                                state_brief=get_bgp_state_brief(
                                    n.get("state", NOT_SET)
                                ),
                                session_state=n.get("state", NOT_SET),
                                state_time=n.get("LastUpDn", NOT_SET),
                                prefix_received=n.get(
                                    "prefixReceived", NOT_SET
                                ),
                                options=options
                            )
                        )

                elif isinstance(
                    v.get("TABLE_vrf", NOT_SET)
                    .get("ROW_vrf", NOT_SET)
                    .get("TABLE_neighbor", NOT_SET)
                    .get("ROW_neighbor", NOT_SET),
                    dict,
                ):
                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=v.get("TABLE_vrf", NOT_SET)
                                    .get("ROW_vrf", NOT_SET)
                                    .get("TABLE_neighbor", NOT_SET)
                                    .get("ROW_neighbor", NOT_SET)
                                    .get("neighbor-id", NOT_SET),
                            peer_hostname=v.get("TABLE_vrf", NOT_SET)
                                        .get("ROW_vrf", NOT_SET)
                                        .get("TABLE_neighbor", NOT_SET)
                                        .get("ROW_neighbor", NOT_SET)
                                        .get("interfaces", NOT_SET),
                            remote_as=v.get("TABLE_vrf", NOT_SET)
                                    .get("ROW_vrf", NOT_SET)
                                    .get("TABLE_neighbor", NOT_SET)
                                    .get("ROW_neighbor", NOT_SET)
                                    .get("remoteas", NOT_SET),
                            state_brief=get_bgp_state_brief(
                                state=v.get("TABLE_vrf", NOT_SET)
                                    .get("ROW_vrf", NOT_SET)
                                    .get("TABLE_neighbor", NOT_SET)
                                    .get("ROW_neighbor", NOT_SET)
                                    .get("state", NOT_SET)
                            ),
                            session_state=v.get("TABLE_vrf", NOT_SET)
                                        .get("ROW_vrf", NOT_SET)
                                        .get("TABLE_neighbor", NOT_SET)
                                        .get("ROW_neighbor", NOT_SET)
                                        .get("state", NOT_SET),
                            state_time=v.get("TABLE_vrf", NOT_SET)
                                        .get("ROW_vrf", NOT_SET)
                                        .get("TABLE_neighbor", NOT_SET)
                                        .get("ROW_neighbor", NOT_SET)
                                        .get("LastUpDn", NOT_SET),
                            prefix_received=v.get("TABLE_vrf", NOT_SET)
                                            .get("ROW_vrf", NOT_SET)
                                            .get("TABLE_neighbor", NOT_SET)
                                            .get("ROW_neighbor", NOT_SET)
                                            .get("prefixReceived", NOT_SET),
                            options=options
                        )
                    )

                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                    BGPSessionsVRF(
                        vrf_name=v.get("TABLE_vrf", NOT_SET)
                                .get("ROW_vrf", NOT_SET)
                                .get("vrf-name-out", NOT_SET),
                        as_number=v.get("TABLE_vrf", NOT_SET)
                                .get("ROW_vrf", NOT_SET)
                                .get("local-as", NOT_SET),
                        router_id=v.get("TABLE_vrf", NOT_SET)
                                .get("ROW_vrf", NOT_SET)
                                .get("router-id", NOT_SET),
                        bgp_sessions=bgp_sessions_lst
                    )
                )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
