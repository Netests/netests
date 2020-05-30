#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF
from netests.converters.vrf.juniper.vrf_juniper_filters import (
    _juniper_vrf_filter,
    _juniper_vrf_default_mapping
)


def _juniper_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    vrf_list = ListVRF(list())

    for vrf in cmd_output.get('instance-information')[0].get('instance-core'):

        if _juniper_vrf_filter(
                vrf.get('instance-name')[0].get('data', NOT_SET)
        ):
            vrf_obj = VRF()

            vrf_obj.vrf_name = _juniper_vrf_default_mapping(
                vrf.get('instance-name')[0].get('data', NOT_SET)
            )
            vrf_obj.vrf_id = vrf.get('router-id')[0].get('data', NOT_SET)
            vrf_obj.vrf_type = vrf.get('instance-type')[0].get('data', NOT_SET)
            vrf_obj.l3_vni = NOT_SET

            if "instance-vrf" in vrf.keys():
                vrf_obj.rd = vrf.get('instance-vrf')[0] \
                                .get('route-distinguisher')[0] \
                                .get('data', NOT_SET)
                vrf_obj.rt_imp = vrf.get('instance-vrf')[0] \
                                    .get('vrf-import')[0] \
                                    .get('data', NOT_SET)
                vrf_obj.rt_exp = vrf.get('instance-vrf')[0]\
                                    .get('vrf-export')[0] \
                                    .get('data', NOT_SET)
                vrf_obj.imp_targ = vrf.get('instance-vrf')[0] \
                                      .get('vrf-import-target')[0] \
                                      .get('data', NOT_SET)
                vrf_obj.exp_targ = vrf.get('instance-vrf')[0] \
                                      .get('vrf-export-target')[0] \
                                      .get('data', NOT_SET)

            vrf_obj.options = options

            vrf_list.vrf_lst.append(vrf_obj)

    return vrf_list
