#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.vrf import VRF, ListVRF
from const.constants import NOT_SET, LEVEL1
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
import pprint
PP = pprint.PrettyPrinter(indent=4)


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

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        PP.pprint(vrf_list.to_json())

    return vrf_list
