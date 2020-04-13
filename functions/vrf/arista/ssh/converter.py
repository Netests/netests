#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from const.constants import NOT_SET, LEVEL1, LEVEL3
from protocols.vrf import VRF, ListVRF
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        print(cmd_output)

    vrf_list = ListVRF(list())
    for vrf_name, facts in cmd_output.get('vrfs').items():

        vrf_obj = VRF(
            vrf_name=vrf_name,
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=facts.get('routeDistinguisher', NOT_SET),
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )

        vrf_list.vrf_lst.append(vrf_obj)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

    return vrf_list
