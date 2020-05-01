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


def _juniper_bgp_ssh_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('bgp'), dict):
            v['bgp'] = json.loads(v.get('bgp'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = json.loads(v.get('rid'))
        if verbose_mode(
            user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
            needed_value=LEVEL3
        ):
            printline()
            PP.pprint(v)

        bgp_sessions_lst = ListBGPSessions(list())
        local_as = ''

        if (
            'bgp' in v.keys() and
            'bgp-peer' in v.get('bgp') \
                           .get('bgp-information')[0] \
                           .keys()
        ):
            for bgp_peer in v.get('bgp') \
                             .get('bgp-information')[0] \
                             .get('bgp-peer'):
                local_as = bgp_peer.get('local-as')[0] \
                                   .get('data', NOT_SET)

                if 'bgp-rib' in bgp_peer.keys():
                    prefix_rcv = bgp_peer.get('bgp-rib')[0] \
                                         .get('received-prefix-count')[0] \
                                         .get('data', NOT_SET)
                else:
                    prefix_rcv = NOT_SET

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=_juniper_bgp_addr_filter(
                        bgp_peer.get('peer-address')[0].get('data', NOT_SET)
                    ),
                    peer_hostname=NOT_SET,
                    remote_as=bgp_peer.get('peer-as')[0].get('data', NOT_SET),
                    state_brief=get_bgp_state_brief(
                        bgp_peer.get('peer-state')[0].get('data', NOT_SET),
                    ),
                    session_state=(
                        bgp_peer.get('peer-state')[0].get('data', NOT_SET)
                    ),
                    state_time=NOT_SET,
                    prefix_received=prefix_rcv,
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

            router_id = NOT_SET
            if (
                'rid' in v.keys() and
                'instance-information' in v.get('rid').keys()
            ):
                router_id = v.get('rid') \
                             .get('instance-information')[0] \
                             .get('instance-core')[0] \
                             .get('router-id')[0] \
                             .get('data', NOT_SET)

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=k,
                as_number=local_as,
                router_id=router_id,
                bgp_sessions=bgp_sessions_lst,
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

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


def _juniper_bgp_addr_filter(ip_addr: str) -> str:
    '''
    This function will remove BGP (tcp) port of output information.
    Juniper output example :

    'peer-address' : [
            {
                'data' : '10.255.255.101+179'
            }
            ],
            'local-address' : [
            {
                'data' : '10.255.255.204+51954'
            }
            ],

    :param ip_addr:
    :return str: IP address without '+port'
    '''

    if ip_addr.find('+') != -1:
        return ip_addr[: ip_addr.find('+')]
    else:
        return ip_addr
