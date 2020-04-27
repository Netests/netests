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
from functions.cli_tools import parse_textfsm
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _extreme_vsp_bgp_ssh_converter(
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

    if cmd_output is not None:
        for vrf in cmd_output:
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
                if v[3] != '':
                    asn = v[1]
                    router_id = v[2]
                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=v[3],
                            peer_hostname=NOT_SET,
                            remote_as=v[4],
                            state_brief=get_bgp_state_brief(v[5]),
                            session_state=v[5],
                            state_time=_extreme_vsp_peer_uptime_converter(
                                day=v[13],
                                hour=v[14],
                                min=v[15],
                                sec=v[16],
                            ),
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
