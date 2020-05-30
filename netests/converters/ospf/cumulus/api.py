#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)


def _cumulus_ospf_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if (
            'ospfd is not running' not in v.get('rid') and
            'ospfd is not running' not in v.get('data') and
            v.get('data') is not None and v.get('rid') is not None and
            v.get('data') != '{\n}' and v.get('data') != '{\n}' and
            v.get('data') != '' and v.get('data') != ''
        ):
            if not isinstance(v.get('rid'), dict):
                v['rid'] = json.loads(v.get('rid'))
            if not isinstance(v.get('data'), dict):
                v['data'] = json.loads(v.get('data'))

            if k != 'default':
                rid = v.get('rid').get(k).get('routerId')
            elif k == 'default':
                rid = v.get('rid').get('routerId')

            o_a_lst = ListOSPFSessionsArea(
                ospf_sessions_area_lst=list()
            )

            if (
                k == 'default' and bool(v.get('data').get('neighbors')) or
                k != 'default' and bool(v.get('data').get(k).get('neighbors'))
            ):
                result_area = dict()
                if k != 'default':
                    neighbors = v.get('data').get(k).get('neighbors')
                elif k == 'default':
                    v.get('data').get('neighbors')

                for r, n in neighbors.items():
                    for i in n:
                        o = OSPFSession(
                            peer_rid=r,
                            peer_hostname=NOT_SET,
                            session_state=i.get('nbrState', NOT_SET),
                            local_interface=i.get('ifaceName', NOT_SET),
                            peer_ip=i.get('ifaceAddress', NOT_SET),
                        )

                        if i.get('areaId') not in result_area.keys():
                            result_area[i.get('areaId')] = OSPFSessionsArea(
                                area_number=i.get('areaId'),
                                ospf_sessions=ListOSPFSessions(
                                    ospf_sessions_lst=list()
                                )
                            )

                        result_area.get(i.get('areaId')).ospf_sessions \
                                                        .ospf_sessions_lst \
                                                        .append(o)

                for area_number, neighbors in result_area.items():
                    o_a_lst.ospf_sessions_area_lst.append(neighbors)

            ospf_vrf_lst.ospf_sessions_vrf_lst.append(
                OSPFSessionsVRF(
                    router_id=rid,
                    vrf_name=k,
                    ospf_sessions_area_lst=o_a_lst
                )
            )

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )
