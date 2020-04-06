#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import (
    NOT_SET,
)
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.global_tools import _generic_state_converter


def _juniper_bgp_ssh_converter(hostname: str(), cmd_outputs: dict) -> BGP:
    if cmd_outputs is None:
        return None

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    for vrf_name in cmd_outputs.keys():

        # Create a BGP sessions list for each VRF
        bgp_sessions_lst = ListBGPSessions(list())
        local_as = ""

        if (
            "bgp-peer"
            in cmd_outputs.get(vrf_name).get("bgp")
            .get("bgp-information")[0].keys()
        ):
            for bgp_peer in (
                cmd_outputs.get(vrf_name)
                .get("bgp")
                .get("bgp-information")[0]
                .get("bgp-peer")
            ):

                local_as = bgp_peer.get("local-as")[0].get("data", NOT_SET)

                if "bgp-rib" in bgp_peer.keys():
                    prefix_received = (
                        bgp_peer.get("bgp-rib")[0]
                        .get("received-prefix-count")[0]
                        .get("data", NOT_SET)
                    )
                else:
                    prefix_received = NOT_SET

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=_juniper_bgp_addr_filter(
                        bgp_peer.get("peer-address")[0].get("data", NOT_SET)
                    ),
                    peer_hostname=NOT_SET,
                    remote_as=bgp_peer.get("peer-as")[0].get("data", NOT_SET),
                    state_brief=_generic_state_converter(
                        bgp_peer.get("peer-state")[0].get("data", NOT_SET),
                    ),
                    session_state=(
                        bgp_peer.get("peer-state")[0].get("data", NOT_SET)
                    ),
                    state_time=NOT_SET,
                    prefix_received=prefix_received,
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

            if vrf_name == "default":
                if "conf" in cmd_outputs.get(vrf_name).keys():
                    if (
                        "configuration" in
                        cmd_outputs.get(vrf_name).get("conf").keys()
                    ):
                        rid = (
                            cmd_outputs.get(vrf_name)
                            .get("conf")
                            .get("configuration")
                            .get("routing-options")
                            .get("router-id")
                        )
                    else:
                        rid = NOT_SET
                else:
                    rid = NOT_SET
            else:
                if "conf" in cmd_outputs.get(vrf_name).keys():
                    if (
                        "configuration" in
                        cmd_outputs.get(vrf_name).get("conf").keys()
                    ):
                        rid = (
                            cmd_outputs.get(vrf_name)
                            .get("conf")
                            .get("configuration")
                            .get("routing-instances")
                            .get("instance")[0]
                            .get("routing-options")
                            .get("router-id", NOT_SET)
                        )
                    else:
                        rid = NOT_SET
                else:
                    rid = NOT_SET

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=vrf_name,
                as_number=local_as,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst,
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)


def _juniper_bgp_addr_filter(ip_addr: str) -> str:
    """
    This function will remove BGP (tcp) port of output information.
    Juniper output example :

    "peer-address" : [
            {
                "data" : "10.255.255.101+179"
            }
            ],
            "local-address" : [
            {
                "data" : "10.255.255.204+51954"
            }
            ],

    :param ip_addr:
    :return str: IP address without "+port"
    """

    if ip_addr.find("+") != -1:
        return ip_addr[: ip_addr.find("+")]
    else:
        return ip_addr
