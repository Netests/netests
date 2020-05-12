#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
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


def _arista_ospf_ssh_converter(
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
        if not isinstance(v.get('rid'), dict):
            v['rid'] = json.loads(v.get('rid'))
        if not isinstance(v.get('data'), dict):
            v['data'] = json.loads(v.get('data'))
        if (
            'vrfs' in v.get('data').keys() and
            'vrfs' in v.get('rid').keys() and
            'errors' not in v.get('data').keys() and
            'errors' not in v.get('rid').keys()
        ):

            o_a_lst = ListOSPFSessionsArea(
                ospf_sessions_area_lst=list()
            )

            result_area = dict()
            for i, ifacts in v.get('data') \
                              .get('vrfs') \
                              .get(k) \
                              .get('instList') \
                              .items():
                for n in ifacts.get('ospfNeighborEntries'):
                    o=OSPFSession(
                        peer_rid=n.get('routerId', NOT_SET),
                        session_state=n.get('adjacencyState', NOT_SET),
                        peer_hostname=NOT_SET,
                        local_interface=n.get('interfaceName', NOT_SET),
                        peer_ip=n.get('interfaceAddress', NOT_SET),
                        options=options
                    )

                    if n.get('details').get('areaId') not in result_area.keys():
                        result_area[n.get('details').get('areaId')] = OSPFSessionsArea(
                            area_number=n.get('details').get('areaId'),
                            ospf_sessions=ListOSPFSessions(
                                ospf_sessions_lst=list()
                            )
                        )

                    result_area.get(
                        n.get('details').get('areaId')
                    ).ospf_sessions.ospf_sessions_lst.append(o)

            for area_number, neighbors in result_area.items():
                    o_a_lst.ospf_sessions_area_lst.append(neighbors)

            rid = NOT_SET
            for j, jfacts in v.get('rid') \
                              .get('vrfs') \
                              .get(k) \
                              .get('instList') \
                              .items():
                rid = jfacts.get('routerId', NOT_SET)

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
