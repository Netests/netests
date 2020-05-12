#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1, LEVEL3
from protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _extreme_vsp_ospf_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        PP.pprint(cmd_output)

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if 'int' in v.keys() and 'data' in v.keys() and 'rid' in v.keys():
            v['data'] = parse_textfsm(
                content=v.get('data'),
                template_file='extreme_vsp_show_ip_ospf_neighbor.textfsm'
            )
            v['rid'] = parse_textfsm(
                content=v.get('rid'),
                template_file='extreme_vsp_show_ip_ospf.textfsm'
            )
            v['int'] = parse_textfsm(
                content=v.get('int'),
                template_file='extreme_vsp_show_ip_ospf_interface.textfsm'
            )

            if (
                len(v.get('data')) > 0 or
                len(v.get('rid')) > 0 or
                len(v.get('int')) > 0
            ):
                ospf_area_lst = ListOSPFSessionsArea(
                    ospf_sessions_area_lst=list()
                )

                for i in v.get('int'):
                    ospf_session_lst = ListOSPFSessions(
                        ospf_sessions_lst=list()
                    )
                    for n in v.get('data'):
                        if i[0] == n[0]:
                            ospf_session_lst.ospf_sessions_lst.append(
                                OSPFSession(
                                    peer_rid=n[1] if n[1] != '' else NOT_SET,
                                    session_state=n[4] if n[4] != '' else NOT_SET,
                                    peer_hostname=NOT_SET,
                                    local_interface=NOT_SET,
                                    peer_ip=n[2] if n[2] != '' else NOT_SET,
                                    options=options
                                )
                            )

                    ospf_area_lst.ospf_sessions_area_lst.append(
                        OSPFSessionsArea(
                            area_number=i[1] if i[1] != '' else NOT_SET,
                            ospf_sessions=ospf_session_lst
                        )
                    )

                rid = NOT_SET
                if len(v.get('rid')) > 0:
                    rid = v.get('rid')[0][0]

                ospf_vrf_lst.ospf_sessions_vrf_lst.append(
                    OSPFSessionsVRF(
                        vrf_name=k,
                        router_id=rid,
                        ospf_sessions_area_lst=ospf_area_lst
                    )
                )

    ospf = OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(ospf.to_json())

    return ospf
