#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
