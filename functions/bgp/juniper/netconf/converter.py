#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.mappings import get_bgp_state_brief
from const.constants import NOT_SET, LEVEL1, LEVEL3
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_bgp_netconf_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('bgp'), dict):
            v['bgp'] = format_xml_output(v.get('bgp'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = format_xml_output(v.get('rid'))
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL3
        ):
            printline()
            PP.pprint(v)
        
        bgp_sessions_lst = ListBGPSessions(
            list()
        )
        print(v)
        if (
            'bgp' in v.keys() and 
            'bgp-information' in v.get('bgp').keys() and
            v.get('bgp').get('bgp-information') is not None and
            'bgp-peer' in v.get('bgp').get('bgp-information').keys()
        ):
            for n in v.get('bgp').get('bgp-information').get('bgp-peer'):
                bgp_sessions_lst.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=n.get('peer-address', NOT_SET),
                        peer_hostname=NOT_SET,
                        remote_as=n.get('peer-as', NOT_SET),
                        state_brief=get_bgp_state_brief(
                            n.get('peer-state', NOT_SET)
                        ),
                        session_state=n.get('peer-state', NOT_SET),
                        state_time=NOT_SET,
                        prefix_received=NOT_SET,
                        options=options
                    )
                )
                as_number = n.get('bgp-option-information').get('local-as')

            router_id = NOT_SET
            if (
                'rid' in v.keys() and
                'instance-information' in v.get('rid').keys() and
                'instance-core' in v.get('rid')
                                    .get('instance-information')
                                    .keys()

            ):
                router_id = v.get('rid') \
                             .get('instance-information') \
                             .get('instance-core') \
                             .get('router-id')

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                BGPSessionsVRF(
                    vrf_name=k,
                    as_number=as_number,
                    router_id=router_id,
                    bgp_sessions=bgp_sessions_lst
                )
            )
            
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
