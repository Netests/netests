#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.mappings import isis_level_converter
from netests.protocols.isis import (
    ISISAdjacency,
    ListISISAdjacency,
    ISISAdjacencyVRF,
    ListISISAdjacencyVRF,
    ISIS
)


def _juniper_isis_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ISIS:

    isis_vrf_lst = ListISISAdjacencyVRF(
        isis_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('data'), dict):
            v['data'] = format_xml_output(v.get('data'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = format_xml_output(v.get('rid'))

        if (
            'output' not in v.get('rid').keys() and
            'IS-IS instance is not running' not in v.get('rid') and
            'output' not in v.get('data').keys() and
            'IS-IS instance is not running' not in v['data']
        ):

            isis_adj_lst = ListISISAdjacency(
                isis_adj_lst=list()
            )

            if 'isis-adjacency-information' in v.get('data'):
                for i in v.get('data') \
                          .get('isis-adjacency-information') \
                          .get('isis-adjacency'):
                    isis_adj_lst.isis_adj_lst.append(
                        ISISAdjacency(
                            session_state=i.get('adjacency-state', NOT_SET),
                            level_type=isis_level_converter(
                                value=i.get('level', NOT_SET)
                            ),
                            circuit_type=i.get('circuit-type', NOT_SET),
                            local_interface_name=i.get(
                                'interface-name', NOT_SET
                            ),
                            neighbor_sys_name=i.get('system-name', NOT_SET),
                            neighbor_ip_addr=i.get('ip-address', NOT_SET),
                            snap=i.get('mac-address', NOT_SET),
                            options=options
                        )
                    )

            print(v.get('rid').keys())

            isis_vrf_lst.isis_vrf_lst.append(
                ISISAdjacencyVRF(
                    router_id=v.get('rid')
                               .get('isis-overview-information')
                               .get('isis-overview')
                               .get('isis-router-id', NOT_SET),
                    system_id=v.get('rid')
                               .get('isis-overview-information')
                               .get('isis-overview')
                               .get('isis-router-sysid', NOT_SET),
                    area_id=v.get('rid')
                               .get('isis-overview-information')
                               .get('isis-overview')
                               .get('isis-router-areaid', NOT_SET),
                    vrf_name=k,
                    adjacencies=isis_adj_lst
                )
            )

    return ISIS(
        isis_vrf_lst=isis_vrf_lst
    )
