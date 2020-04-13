#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from protocols.vrf import VRF, ListVRF
from const.constants import NOT_SET as NSET


def _napalm_vrf_converter(
    hostname: str(),
    cmd_output: json,
    options={}
) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('get_network_instances'):

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf,
                vrf_type=cmd_output.get('get_network_instances')
                                   .get(vrf)
                                   .get('type', NSET),
                rd=cmd_output.get('get_network_instances')
                             .get(vrf)
                             .get('state')
                             .get('route_distinguisher')
                                if cmd_output.get('get_network_instances')
                                             .get(vrf)
                                             .get('state')
                                             .get('route_distinguisher', NSET)
                                                != "" else NSET
            )
        )

    return vrf_list


def _arista_vrf_converter(
    hostname: str(),
    cmd_output: json,
    options={}
) -> ListVRF:

    vrf_list = ListVRF(list())

    for vrf_name, facts in cmd_output.get('vrfs').items():

        vrf_obj = VRF(
            vrf_name=vrf_name,
            rd=facts.get('routeDistinguisher', NSET)
        )

        vrf_list.vrf_lst.append(vrf_obj)

    return vrf_list
