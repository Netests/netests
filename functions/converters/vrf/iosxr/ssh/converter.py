#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    LEVEL4,
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


def _iosxr_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    cmd_output = re.sub(
        pattern=r"communities:[\n\r]\s+RT",
        repl="communities:RT",
        string=cmd_output
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(cmd_output)

    template = open(
        f"{TEXTFSM_PATH}cisco_xr_show_vrf_all_detail.textfsm")
    results_template = textfsm.TextFSM(template)
    parsed_results = results_template.ParseText(cmd_output)

    list_vrf = ListVRF(list())

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        print(parsed_results)

    for nei in parsed_results:
        vrf = VRF(
            vrf_name=nei[0]
                if nei[0] != "not set" and nei[0] != '' else NOT_SET,
            vrf_id=NOT_SET,
            vrf_type=nei[3]
                if nei[3] != "not set" and nei[3] != '' else NOT_SET,
            l3_vni=NOT_SET,
            rd=nei[1] if nei[1] != "not set" and nei[1] != '' else NOT_SET,
            rt_imp=nei[5] if nei[5] != "not set" and nei[5] != '' else NOT_SET,
            rt_exp=nei[6] if nei[6] != "not set" and nei[6] != '' else NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )

        list_vrf.vrf_lst.append(vrf)

    return list_vrf
