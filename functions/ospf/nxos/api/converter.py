#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL1
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


def _nxos_ospf_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('data'), dict):
            v['data'] = json.loads(v.get('data'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = json.loads(v.get('rid'))

        if (
            v.get('data')
             .get('ins_api')
             .get('outputs')
             .get('output')
             .get('code') == '200' and 
            v.get('rid')
             .get('ins_api')
             .get('outputs')
             .get('output')
             .get('code') == '200' and
            isinstance(
                v.get('data')
                 .get('ins_api')
                 .get('outputs')
                 .get('output')
                 .get('body'),
                dict
            )
        ):
            
            PP.pprint(v)

            o_a_lst = ListOSPFSessionsArea(
                ospf_sessions_area_lst=list()
            )
            result_area = dict()
            
            if isinstance(
                v.get('data')
                 .get('ins_api')
                 .get('outputs')
                 .get('output')
                 .get('body')
                 .get('TABLE_ctx')
                 .get('ROW_ctx')
                 .get('TABLE_nbr')
                 .get('ROW_nbr'),
                dict
            ):
                o = OSPFSession(
                    peer_rid=v.get('data')
                              .get('ins_api')
                              .get('outputs')
                              .get('output')
                              .get('body')
                              .get('TABLE_ctx')
                              .get('ROW_ctx')
                              .get('TABLE_nbr')
                              .get('ROW_nbr')
                              .get('rid', NOT_SET),
                    peer_hostname=NOT_SET,
                    session_state=v.get('data')
                                   .get('ins_api')
                                   .get('outputs')
                                   .get('output')
                                   .get('body')
                                   .get('TABLE_ctx')
                                   .get('ROW_ctx')
                                   .get('TABLE_nbr')
                                   .get('ROW_nbr')
                                   .get('state', NOT_SET),
                    local_interface=v.get('data')
                                     .get('ins_api')
                                     .get('outputs')
                                     .get('output')
                                     .get('body')
                                     .get('TABLE_ctx')
                                     .get('ROW_ctx')
                                     .get('TABLE_nbr')
                                     .get('ROW_nbr')
                                     .get('intf', NOT_SET),
                    peer_ip=v.get('data')
                             .get('ins_api')
                             .get('outputs')
                             .get('output')
                             .get('body')
                             .get('TABLE_ctx')
                             .get('ROW_ctx')
                             .get('TABLE_nbr')
                             .get('ROW_nbr')
                             .get('addr', NOT_SET),
                )

                if (
                    v.get('data')
                     .get('ins_api')
                     .get('outputs')
                     .get('output')
                     .get('body')
                     .get('TABLE_ctx')
                     .get('ROW_ctx')
                     .get('TABLE_nbr')
                     .get('ROW_nbr')
                     .get('area', NOT_SET) not in result_area.keys()
                ):
                    result_area[v.get('data')
                                 .get('ins_api')
                                 .get('outputs')
                                 .get('output')
                                 .get('body')
                                 .get('TABLE_ctx')
                                 .get('ROW_ctx')
                                 .get('TABLE_nbr')
                                 .get('ROW_nbr')
                                 .get('area', NOT_SET)] = OSPFSessionsArea(
                        area_number=v.get('data')
                                     .get('ins_api')
                                     .get('outputs')
                                     .get('output')
                                     .get('body')
                                     .get('TABLE_ctx')
                                     .get('ROW_ctx')
                                     .get('TABLE_nbr')
                                     .get('ROW_nbr')
                                     .get('area', NOT_SET),
                        ospf_sessions=ListOSPFSessions(
                            ospf_sessions_lst=list()
                        )
                    )

                    result_area.get(v.get('data')
                                     .get('ins_api')
                                     .get('outputs')
                                     .get('output')
                                     .get('body')
                                     .get('TABLE_ctx')
                                     .get('ROW_ctx')
                                     .get('TABLE_nbr')
                                     .get('ROW_nbr')
                                     .get('area', NOT_SET)
                                    ).ospf_sessions.ospf_sessions_lst.append(o)

            elif isinstance(
                v.get('data')
                 .get('ins_api')
                 .get('outputs')
                 .get('output')
                 .get('body')
                 .get('TABLE_ctx')
                 .get('ROW_ctx')
                 .get('TABLE_nbr')
                 .get('ROW_nbr'),
                list
            ):
                for n in v.get('data') \
                          .get('ins_api') \
                          .get('outputs') \
                          .get('output') \
                          .get('body') \
                          .get('TABLE_ctx') \
                          .get('ROW_ctx') \
                          .get('TABLE_nbr') \
                          .get('ROW_nbr'):

                    o = OSPFSession(
                        peer_rid=n.get('rid', NOT_SET),
                        peer_hostname=NOT_SET,
                        session_state=n.get('state', NOT_SET),
                        local_interface=n.get('intf', NOT_SET),
                        peer_ip=n.get('addr', NOT_SET),
                    )

                    if n.get('area', NOT_SET) not in result_area.keys():
                        result_area[n.get('area', NOT_SET)] = OSPFSessionsArea(
                            area_number=n.get('area', NOT_SET),
                            ospf_sessions=ListOSPFSessions(
                                ospf_sessions_lst=list()
                            )
                        )

                    result_area.get(
                        n.get('area', NOT_SET)
                    ).ospf_sessions.ospf_sessions_lst.append(o)

            if 'ins_api' in v.get('rid').keys():
                rid = v.get('rid') \
                       .get('ins_api') \
                       .get('outputs') \
                       .get('output') \
                       .get('body') \
                       .get('TABLE_ctx') \
                       .get('ROW_ctx') \
                       .get('rid', NOT_SET)
            else:
                rid = NOT_SET

            for area_number, neighbors in result_area.items():
                    o_a_lst.ospf_sessions_area_lst.append(neighbors)

            ospf_vrf_lst.ospf_sessions_vrf_lst.append(
                OSPFSessionsVRF(
                    router_id=rid,
                    vrf_name=k,
                    ospf_sessions_area_lst=o_a_lst
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
