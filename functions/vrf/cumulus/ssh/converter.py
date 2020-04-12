#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import printline
from functions.verbose_mode import (
    verbose_mode
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _cumulus_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:
    template = open(
        f"{TEXTFSM_PATH}cumulus_net_show_vrf.textfsm"
    )
    results_template = textfsm.TextFSM(template)
    parsed_results = results_template.ParseText(cmd_output)

    vrf_list = ListVRF(list())

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        print(parsed_results)

    for line in parsed_results:
        vrf = VRF(
            vrf_name=line[0],
            vrf_id=line[1],
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )

        vrf_list.vrf_lst.append(vrf)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

    return vrf_list
