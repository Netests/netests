#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)


def _juniper_ospf_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('data'), dict):
            v['data'] = format_xml_output(v.get('data'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = format_xml_output(v.get('rid'))

        if (
            'output' not in v.get('data').keys() and
            'output' not in v.get('rid').keys()
        ):

            o_a_lst = ListOSPFSessionsArea(
                ospf_sessions_area_lst=list()
            )

            if 'ospf-neighbor-information' in v.get('data').keys():
                result_area = dict()
                for n in v.get('data').get('ospf-neighbor-information') \
                                      .get('ospf-neighbor'):
                    o = OSPFSession(
                        peer_rid=n.get('neighbor-id', NOT_SET),
                        peer_hostname=NOT_SET,
                        session_state=n.get('ospf-neighbor-state', NOT_SET),
                        local_interface=n.get('interface-name', NOT_SET),
                        peer_ip=n.get('neighbor-address', NOT_SET),
                    )

                    if n.get('ospf-area') not in result_area.keys():
                        result_area[n.get('ospf-area')] \
                            = OSPFSessionsArea(
                            area_number=n.get('ospf-area'),
                            ospf_sessions=ListOSPFSessions(
                                ospf_sessions_lst=list()
                            )
                        )

                    result_area.get(
                        n.get('ospf-area')
                    ).ospf_sessions.ospf_sessions_lst.append(o)

                for area_number, neighbors in result_area.items():
                    o_a_lst.ospf_sessions_area_lst.append(neighbors)

            if 'ospf-overview-information' in v.get('rid').keys():
                rid = v.get('rid') \
                       .get('ospf-overview-information') \
                       .get('ospf-overview') \
                       .get('ospf-router-id')
            else:
                rid = NOT_SET

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
