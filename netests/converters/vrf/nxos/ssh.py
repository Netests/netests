#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF


def _nxos_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    vrf_list = ListVRF(list())
    for vrf in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf'):
        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf.get('vrf_name', NOT_SET),
                vrf_id=vrf.get('vrf_id', NOT_SET),
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=vrf.get('rd') if vrf.get('rd') != '0:0' else NOT_SET,
                rt_imp=NOT_SET,
                rt_exp=NOT_SET,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET,
                options=options
            )
        )

    return vrf_list
