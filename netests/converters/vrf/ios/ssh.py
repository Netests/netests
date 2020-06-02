#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from netests.constants import NOT_SET as NSET
from netests.tools.cli import parse_textfsm
from netests.protocols.vrf import VRF, ListVRF


def _ios_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    cmd_output = re.sub(
        pattern=r"communities[\n\r]\s+RT",
        repl="communities:RT",
        string=cmd_output
    )

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file='cisco_ios_show_ip_vrf_detail.textfsm'
    )

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
            imp_targ=NSET,
            options=options
        )
    )

    for nei in cmd_output:
        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=nei[0]
                    if nei[0] != "<not set>" and nei[0] != '' else NSET,
                vrf_id=nei[1]
                    if nei[1] != "<not set>" and nei[1] != '' else NSET,
                vrf_type=NSET,
                l3_vni=NSET,
                rd=nei[2] if nei[2] != "<not set>" and nei[2] != '' else NSET,
                rt_imp=nei[5]
                    if nei[5] != "<not set>" and nei[5] != '' else NSET,
                rt_exp=nei[6]
                    if nei[6] != "<not set>" and nei[6] != '' else NSET,
                exp_targ=NSET,
                imp_targ=NSET,
                options=options
            )
        )

    return vrf_list
