#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF


def _napalm_vrf_converter(
    hostname: str(),
    cmd_output: dict,
    options={}
) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('get_network_instances'):

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf,
                vrf_type=cmd_output.get('get_network_instances')
                                   .get(vrf)
                                   .get('type', NOT_SET),
                rd=cmd_output.get('get_network_instances')
                             .get(vrf)
                             .get('state')
                             .get('route_distinguisher')
                if cmd_output.get('get_network_instances')
                .get(vrf)
                .get('state')
                .get('route_distinguisher', NOT_SET)
                != "" else NOT_SET
            )
        )

    return vrf_list
