#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.mappings import isis_level_converter
from netests.protocols.isis import (
    ISISAdjacency,
    ListISISAdjacency,
    ISISAdjacencyVRF,
    ListISISAdjacencyVRF,
    ISIS
)


def _juniper_isis_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ISIS:

    isis_vrf_lst = ListISISAdjacencyVRF(
        isis_vrf_lst=list()
    )

    for k, v in cmd_output.items():
        if not isinstance(v.get('data'), dict):
            v['data'] = json.loads(v.get('data'))
        if not isinstance(v.get('rid'), dict):
            v['rid'] = json.loads(v.get('rid'))

        if (
            'output' not in v.get('rid').keys() and
            'output' not in v.get('data').keys()
        ):

            isis_adj_lst = ListISISAdjacency(
                isis_adj_lst=list()
            )

            if (
                'isis-adjacency-information' in v.get('data').keys() and
                'isis-adjacency' in v.get('data')
                                     .get('isis-adjacency-information')[0]
                                     .keys()
            ):
                for i in v.get('data') \
                          .get('isis-adjacency-information')[0] \
                          .get('isis-adjacency'):
                    isis_adj_lst.isis_adj_lst.append(
                        ISISAdjacency(
                            session_state=i.get('adjacency-state')[0]
                                           .get('data')
                            if 'adjacency-state' in i.keys() else NOT_SET,
                            level_type=isis_level_converter(
                                value=i.get('level')[0].get('data')
                            ) if 'level' in i.keys() else NOT_SET,
                            circuit_type=i.get('circuit-type')[0].get('data')
                            if 'circuit-type' in i.keys() else NOT_SET,
                            local_interface_name=i.get('interface-name')[0]
                                                  .get('data')
                            if 'interface-name' in i.keys() else NOT_SET,
                            neighbor_sys_name=i.get('system-name')[0]
                                               .get('data')
                            if 'interface-name' in i.keys() else NOT_SET,
                            neighbor_ip_addr=i.get('ip-address')[0].get('data')
                            if 'ip-address' in i.keys() else NOT_SET,
                            snap=i.get('mac-address')[0].get('data')
                            if 'mac-address' in i.keys() else NOT_SET,
                            options=options
                        )
                    )

                isis_vrf_lst.isis_vrf_lst.append(
                    ISISAdjacencyVRF(
                        router_id=v.get('rid')
                                .get('isis-overview-information')[0]
                                .get('isis-overview')[0]
                                .get('isis-router-id')[0]
                                .get('data', NOT_SET),
                        system_id=v.get('rid')
                                .get('isis-overview-information')[0]
                                .get('isis-overview')[0]
                                .get('isis-router-sysid')[0]
                                .get('data', NOT_SET),
                        area_id=v.get('rid')
                                .get('isis-overview-information')[0]
                                .get('isis-overview')[0]
                                .get('isis-router-areaid')[0]
                                .get('data', NOT_SET),
                        vrf_name=k,
                        adjacencies=isis_adj_lst
                    )
                )

    return ISIS(
        isis_vrf_lst=isis_vrf_lst
    )
