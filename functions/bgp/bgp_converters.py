#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from const.constants import (
    NOT_SET,
    BGP_STATE_UP_LIST,
    BGP_STATE_BRIEF_UP,
    BGP_STATE_BRIEF_DOWN,
)
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP,
)
from functions.global_tools import _generic_state_converter


ERROR_HEADER = "Error import [bgp_converters.py]"
HEADER_GET = "[netests - bgp_converters]"


def _napalm_bgp_status_converter(status: str) -> str:
    """
    This function is used to standardize BGP sessions state.
    Napalm use is_up=True and is_enable=True to simplify BGP state.
    In this project we use "UP/DOWN".

    'is_enabled': True,
    'is_up': True,

    :param status:
    :return str: Standard name of BGP state
    """
    if str(status).upper() == "TRUE":
        return "UP"
    elif str(status).upper() == "FALSE":
        return "DOWN"
    else:
        return status


def _napalm_bgp_vrf_converter(vrf_name: str) -> str:
    """
    This function is used to standardize Global routing table name (vrf_name).
    Napalm named this routing table "global".
    Other word is "global", "grt" or "default".
    In this project we use "default".

    :param vrf_name:
    :return str: Global/Default routing table name
    """

    if str(vrf_name).upper() == "GLOBAL" or str(vrf_name).upper() == "GRT":
        return "default"
    else:
        return vrf_name


def _napalm_bgp_converter(hostname: str(), cmd_output: json) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    local_as = ""

    if "get_bgp_neighbors" in cmd_output.keys():

        for vrf_name, vrf_facts in cmd_output.get("get_bgp_neighbors").items():

            bgp_sessions_lst = ListBGPSessions(list())

            for peer_ip, facts in vrf_facts.get("peers").items():

                bgp_obj = BGPSession(
                    src_hostname=hostname,
                    peer_ip=peer_ip,
                    peer_hostname=facts.get("hostname", NOT_SET),
                    remote_as=facts.get("remote_as", NOT_SET),
                    state_brief=_napalm_bgp_status_converter(
                        facts.get("is_up", NOT_SET)
                    ),
                    session_state=facts.get("session_state", NOT_SET),
                    state_time=facts.get("uptime", NOT_SET),
                    prefix_received=facts.get("address_family")
                    .get("ipv4")
                    .get("received_prefixes"),
                )

                local_as = facts.get("local_as", NOT_SET)

                bgp_sessions_lst.bgp_sessions.append(bgp_obj)

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=_napalm_bgp_vrf_converter(vrf_name),
                as_number=local_as,
                router_id=vrf_facts.get("router_id"),
                bgp_sessions=bgp_sessions_lst,
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)

def _nexus_bgp_converter(hostname: str(), cmd_outputs: list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        if isinstance(
            cmd_output.get("TABLE_vrf").get("ROW_vrf").get("TABLE_neighbor")
            .get("ROW_neighbor", NOT_SET),
            list,
        ):
            for neighbor in (
                cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
            ):

                if neighbor.get("state", NOT_SET) in BGP_STATE_UP_LIST:
                    state_brief = BGP_STATE_BRIEF_UP
                else:
                    state_brief = BGP_STATE_BRIEF_DOWN

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=neighbor.get("neighbor-id", NOT_SET),
                    peer_hostname=neighbor.get("interfaces", NOT_SET),
                    remote_as=neighbor.get("remoteas", NOT_SET),
                    state_brief=state_brief,
                    session_state=neighbor.get("state", NOT_SET),
                    state_time=neighbor.get("LastUpDn", NOT_SET),
                    prefix_received=neighbor.get("prefixReceived", NOT_SET),
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

        elif isinstance(
            cmd_output.get("TABLE_vrf", NOT_SET)
            .get("ROW_vrf", NOT_SET)
            .get("TABLE_neighbor", NOT_SET)
            .get("ROW_neighbor", NOT_SET),
            dict,
        ):

            if (
                cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("state", NOT_SET)
                in BGP_STATE_UP_LIST
            ):
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("neighbor-id", NOT_SET),
                peer_hostname=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("interfaces", NOT_SET),
                remote_as=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("remoteas", NOT_SET),
                state_brief=state_brief,
                session_state=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("state", NOT_SET),
                state_time=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("LastUpDn", NOT_SET),
                prefix_received=cmd_output.get("TABLE_vrf", NOT_SET)
                .get("ROW_vrf", NOT_SET)
                .get("TABLE_neighbor", NOT_SET)
                .get("ROW_neighbor", NOT_SET)
                .get("prefixReceived", NOT_SET),
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=cmd_output.get("TABLE_vrf", NOT_SET)
            .get("ROW_vrf", NOT_SET)
            .get("vrf-name-out", NOT_SET),
            as_number=cmd_output.get("TABLE_vrf", NOT_SET)
            .get("ROW_vrf", NOT_SET)
            .get("local-as", NOT_SET),
            router_id=cmd_output.get("TABLE_vrf", NOT_SET)
            .get("ROW_vrf", NOT_SET)
            .get("router-id", NOT_SET),
            bgp_sessions=bgp_sessions_lst,
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS BGP Converter
#
def _ios_bgp_converter(hostname: str(), cmd_outputs: dict) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    for vrf in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        for bgp_session in cmd_outputs.get(vrf):

            state_brief = BGP_STATE_BRIEF_UP
            asn = bgp_session[1]
            rid = bgp_session[0]

            if str(bgp_session[5]).isdigit() is False:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_sessions_lst.bgp_sessions.append(
                BGPSession(
                    src_hostname=hostname,
                    peer_ip=bgp_session[2],
                    peer_hostname=NOT_SET,
                    remote_as=bgp_session[3],
                    state_brief=state_brief,
                    session_state=bgp_session[5],
                    state_time=bgp_session[4],
                    prefix_received=NOT_SET,
                )
            )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
            BGPSessionsVRF(
                vrf_name=vrf,
                as_number=asn,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst,
            )
        )

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista BGP Converter
#
def _arista_bgp_converter(hostname: str(), cmd_outputs: list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        temp_value = cmd_output.get("vrfs").keys()
        for key in temp_value:
            vrf_name = key
            break

        for neighbor, facts in (
            cmd_output.get("vrfs", NOT_SET)
            .get(vrf_name, NOT_SET)
            .get("peers", NOT_SET)
            .items()
        ):

            if facts.get("peerState", NOT_SET) in BGP_STATE_UP_LIST:
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=neighbor,
                peer_hostname=facts.get("hostname", NOT_SET),
                remote_as=facts.get("asn", NOT_SET),
                state_brief=state_brief,
                session_state=facts.get("peerState", NOT_SET),
                state_time=facts.get("upDownTime", NOT_SET),
                prefix_received=facts.get("prefixReceived", NOT_SET),
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=vrf_name,
            as_number=cmd_output.get("vrfs", NOT_SET)
            .get(vrf_name, NOT_SET)
            .get("asn", NOT_SET),
            router_id=cmd_output.get("vrfs", NOT_SET)
            .get(vrf_name, NOT_SET)
            .get("routerId", NOT_SET),
            bgp_sessions=bgp_sessions_lst,
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)


def _extreme_vsp_bgp_converter(hostname: str(), cmd_outputs: dict) -> BGP:

    if cmd_outputs is None:
        return None

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    for vrf in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        i = 1

        for bgp_session in cmd_outputs.get(vrf):

            # To remove last line empty ...
            if len(cmd_outputs.get(vrf)) - i > 0:

                asn = bgp_session[1]
                rid = bgp_session[2]

                bgp_sessions_lst.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=bgp_session[3],
                        peer_hostname=NOT_SET,
                        remote_as=bgp_session[4],
                        state_brief=_generic_state_converter(bgp_session[5]),
                        session_state=bgp_session[5],
                        state_time=_extreme_vsp_peer_uptime_converter(
                            day=bgp_session[13],
                            hour=bgp_session[14],
                            min=bgp_session[15],
                            sec=bgp_session[16],
                        ),
                        prefix_received=NOT_SET,
                    )
                )

                i += 1

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
            BGPSessionsVRF(
                vrf_name=vrf,
                as_number=asn,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst,
            )
        )

    return BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)


def _extreme_vsp_peer_uptime_converter(day, hour, min, sec) -> str:
    """
    This function will convert BGP peer uptime from an
    Extreme VSP output command.
    Output example:

        - 0 day(s), 00:42:05

    :param day:
    :param hour:
    :param min:
    :param sec:
    :return str: All convert in second
    """

    return str(
        (
            int(_extreme_vsp_remove_double_zero(day)) * 24 * 60 * 60
            + int(_extreme_vsp_remove_double_zero(hour)) * 60 * 60
        )
        + int(_extreme_vsp_remove_double_zero(min)) * 60
        + int(_extreme_vsp_remove_double_zero(sec))
    )


def _extreme_vsp_remove_double_zero(value) -> str:
    """
    This function will remove a zero of the peer uptime value.
    This operation is necessary to convert str to int.

    :param value:
    :return str: value if not 00 else 0
    """

    return value if value != "00" else "0"
