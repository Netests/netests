#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from netests.tools.cli import parse_textfsm
from netests.mappings import get_bgp_state_brief
from netests.constants import NOT_SET


def _extreme_vsp_bgp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    if cmd_output is not None:
        for vrf in cmd_output:
            if (
                "BGP instance does not exist" not in cmd_output.get(vrf) and
                "cannot be accessed by name" not in cmd_output.get(vrf)
            ):
                cmd_output[vrf] = parse_textfsm(
                    content=str(cmd_output[vrf]),
                    template_file="extreme_vsp_show_ip_bgp_summary.textfsm"
                )
                bgp_sessions_lst = ListBGPSessions(
                    bgp_sessions=list()
                )
                asn = NOT_SET
                router_id = NOT_SET

                for v in cmd_output.get(vrf):
                    asn = v[1] if v[1] != '' else NOT_SET
                    router_id = v[2] if v[2] != '' else NOT_SET
                    if v[3] != '':
                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=v[3] if v[3] != '' else NOT_SET,
                                peer_hostname=NOT_SET,
                                remote_as=v[4],
                                state_brief=get_bgp_state_brief(v[5]),
                                session_state=v[5] if v[5] != '' else NOT_SET,
                                state_time=_extreme_vsp_peer_uptime_converter(
                                    day=v[13],
                                    hour=v[14],
                                    min=v[15],
                                    sec=v[16],
                                ) if v[13] != '' else NOT_SET,
                                prefix_received=NOT_SET,
                            )
                        )

                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                    BGPSessionsVRF(
                        vrf_name=vrf,
                        as_number=asn,
                        router_id=router_id,
                        bgp_sessions=bgp_sessions_lst,
                    )
                )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )


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
    :return str: All convert in msecond
    """
    return str(
        (
            (
                int(_extreme_vsp_remove_double_zero(day)) * 24 * 60 * 60
                + int(_extreme_vsp_remove_double_zero(hour)) * 60 * 60
            )
            + int(_extreme_vsp_remove_double_zero(min)) * 60
            + int(_extreme_vsp_remove_double_zero(sec))
        )
        * 1000
    )


def _extreme_vsp_remove_double_zero(value) -> str:
    """
    This function will remove a zero of the peer uptime value.
    This operation is necessary to convert str to int.

    :param value:
    :return str: value if not 00 else 0
    """

    return value if value != "00" else "0"
