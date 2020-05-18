#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
from functions.mappings import get_bgp_state_brief
from const.constants import NOT_SET, LEVEL1, LEVEL3
from functions.verbose_mode import verbose_mode
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_bgp_api_converter(
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
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL3
        ):
            printline()
            PP.pprint(v)

        if (
            'ins_api' in v.keys() and
            'outputs' in v.get('ins_api').keys() and
            'output' in v.get('ins_api').get('outputs').keys() and
            'body' in v.get('ins_api').get('outputs').get('output').keys() and
            v.get('ins_api').get('outputs').get('output').get('code') == '200'
        ):
            bgp_vrf = BGPSessionsVRF(
                vrf_name=v.get('ins_api')
                          .get('outputs')
                          .get('output')
                          .get('body')
                          .get('TABLE_vrf')
                          .get('ROW_vrf')
                          .get('vrf-name-out', NOT_SET),
                as_number=v.get('ins_api')
                          .get('outputs')
                          .get('output')
                          .get('body')
                          .get('TABLE_vrf')
                          .get('ROW_vrf')
                          .get('local-as', NOT_SET),
                router_id=v.get('ins_api')
                          .get('outputs')
                          .get('output')
                          .get('body')
                          .get('TABLE_vrf')
                          .get('ROW_vrf')
                          .get('router-id', NOT_SET),
                bgp_sessions=ListBGPSessions(
                    bgp_sessions=list()
                )
            )

            if isinstance(
                v.get('ins_api')
                 .get('outputs')
                 .get('output')
                 .get('body')
                 .get('TABLE_vrf')
                 .get('ROW_vrf')
                 .get('TABLE_neighbor')
                 .get('ROW_neighbor'),
                dict
            ):
                bgp_vrf.bgp_sessions.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=v.get('ins_api')
                                 .get('outputs')
                                 .get('output')
                                 .get('body')
                                 .get('TABLE_vrf')
                                 .get('ROW_vrf')
                                 .get('TABLE_neighbor')
                                 .get('ROW_neighbor')
                                 .get('neighbor-id'),
                        peer_hostname=NOT_SET,
                        remote_as=v.get('ins_api')
                                   .get('outputs')
                                   .get('output')
                                   .get('body')
                                   .get('TABLE_vrf')
                                   .get('ROW_vrf')
                                   .get('TABLE_neighbor')
                                   .get('ROW_neighbor')
                                   .get('remoteas'),
                        state_brief=get_bgp_state_brief(
                            state=v.get('ins_api')
                                   .get('outputs')
                                   .get('output')
                                   .get('body')
                                   .get('TABLE_vrf')
                                   .get('ROW_vrf')
                                   .get('TABLE_neighbor')
                                   .get('ROW_neighbor')
                                   .get('state')
                        ),
                        session_state=v.get('ins_api')
                                       .get('outputs')
                                       .get('output')
                                       .get('body')
                                       .get('TABLE_vrf')
                                       .get('ROW_vrf')
                                       .get('TABLE_neighbor')
                                       .get('ROW_neighbor')
                                       .get('state'),
                        state_time=v.get('ins_api')
                                    .get('outputs')
                                    .get('output')
                                    .get('body')
                                    .get('TABLE_vrf')
                                    .get('ROW_vrf')
                                    .get('TABLE_neighbor')
                                    .get('ROW_neighbor')
                                    .get('lastflap'),
                        prefix_received=NOT_SET,
                        options=options
                    )
                )

            elif isinstance(
                v.get('ins_api')
                 .get('outputs')
                 .get('output')
                 .get('body')
                 .get('TABLE_vrf')
                 .get('ROW_vrf')
                 .get('TABLE_neighbor')
                 .get('ROW_neighbor'),
                 list
            ):
                for n in v.get('ins_api') \
                          .get('outputs') \
                          .get('output') \
                          .get('body') \
                          .get('TABLE_vrf') \
                          .get('ROW_vrf') \
                          .get('TABLE_neighbor') \
                          .get('ROW_neighbor'):
                    bgp_vrf.bgp_sessions.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=n.get('neighbor-id'),
                            peer_hostname=NOT_SET,
                            remote_as=n.get('remoteas'),
                            state_brief=get_bgp_state_brief(
                                state=n.get('state')
                            ),
                            session_state=n.get('state'),
                            state_time=n.get('lastflap'),
                            prefix_received=NOT_SET,
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
