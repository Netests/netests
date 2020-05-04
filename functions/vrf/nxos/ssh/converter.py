#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from const.constants import NOT_SET, LEVEL1
from protocols.vrf import VRF, ListVRF
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:
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

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

    return vrf_list
