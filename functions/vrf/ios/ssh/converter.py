#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import textfsm
from const.constants import (
    NOT_SET as NSET,
    LEVEL1,
    LEVEL4,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_vrf_ssh_converter(hostname: str(), cmd_output: list) -> ListVRF:
    cmd_output = re.sub(
        pattern=r"communities[\n\r]\s+RT",
        repl="communities:RT",
        string=cmd_output
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NSET),
        needed_value=LEVEL4
    ):
        printline()
        print(cmd_output)

    template = open(
        f"{TEXTFSM_PATH}cisco_ios_show_ip_vrf_detail.textfsm")
    results_template = textfsm.TextFSM(template)
    # Example : [
    #   ['mgmt', '1', '<not set>'],
    #   ['tenant-1', '2', '10.255.255.103:103']
    # ]
    parsed_results = results_template.ParseText(cmd_output)

    vrf_list = ListVRF(list())
    # Add the default VRF maually
    vrf_list.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="0",
            vrf_type=NSET,
            l3_vni=NSET,
            rd=NSET,
            rt_imp=NSET,
            rt_exp=NSET,
            exp_targ=NSET,
            imp_targ=NSET
        )
    )

    for l in parsed_results:
        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=l[0] if l[0] != "<not set>" and l[0] != '' else NSET,
                vrf_id=l[1] if l[1] != "<not set>" and l[1] != '' else NSET,
                vrf_type=NSET,
                l3_vni=NSET,
                rd=l[2] if l[2] != "<not set>" and l[2] != '' else NSET,
                rt_imp=l[5] if l[5] != "<not set>" and l[5] != '' else NSET,
                rt_exp=l[6] if l[6] != "<not set>" and l[6] != '' else NSET,
                exp_targ=NSET,
                imp_targ=NSET
            )
        )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NSET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

    return vrf_list
