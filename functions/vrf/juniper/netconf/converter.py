#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from const.constants import (
    NOT_SET,
    LEVEL3,
    LEVEL4
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.vrf.juniper.vrf_juniper_filters import (
    _juniper_vrf_filter,
    _juniper_vrf_default_mapping
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_vrf_netconf_converter(hostname: str, cmd_output: list) -> ListVRF:
    cmd_output = json.loads(cmd_output)
    if verbose_mode(
        user_value=os.environ["NETESTS_VERBOSE"],
        needed_value=LEVEL4
    ):
        printline()
        PP.pprint(cmd_output)

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('instance-information').get('instance-core'):
        if _juniper_vrf_filter(vrf.get('instance-name')):
            vrf_obj = VRF()

            vrf_obj.vrf_name = _juniper_vrf_default_mapping(
                vrf.get('instance-name')
            )
            vrf_obj.vrf_id = vrf.get('router-id', NOT_SET)
            vrf_obj.vrf_type = vrf.get('instance-type', NOT_SET)
            vrf_obj.l3_vni = NOT_SET

            if "instance-vrf" in vrf.keys():
                vrf_obj.rd = vrf.get('instance-vrf') \
                                .get('route-distinguisher', NOT_SET)
                vrf_obj.rt_imp = vrf.get('instance-vrf') \
                                    .get('vrf-import', NOT_SET)
                vrf_obj.rt_exp = vrf.get('instance-vrf') \
                                    .get('vrf-export', NOT_SET)
                vrf_obj.exp_targ = vrf.get('instance-vrf') \
                                      .get('vrf-import-target', NOT_SET)
                vrf_obj.exp_targ = vrf.get('instance-vrf') \
                                      .get('vrf-export-target', NOT_SET)

            vrf_list.vrf_lst.append(vrf_obj)

    if verbose_mode(
        user_value=os.environ["NETESTS_VERBOSE"],
        needed_value=LEVEL3
    ):
        printline()
        print(vrf_list)

    return vrf_list
