#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.vrf import VRF, ListVRF


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

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file='cisco_xr_show_vrf_all_detail.textfsm'
    )

    list_vrf = ListVRF(list())

    list_vrf.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            l3_vni=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )
    )

    for nei in cmd_output:
        list_vrf.vrf_lst.append(
            VRF(
                vrf_name=nei[0]
                    if nei[0] != "not set" and nei[0] != '' else NOT_SET,
                vrf_id=NOT_SET,
                vrf_type=nei[3]
                    if nei[3] != "not set" and nei[3] != '' else NOT_SET,
                l3_vni=NOT_SET,
                rd=nei[1]
                    if nei[1] != "not set" and nei[1] != '' else NOT_SET,
                rt_imp=nei[5]
                    if nei[5] != "not set" and nei[5] != '' else NOT_SET,
                rt_exp=nei[6]
                    if nei[6] != "not set" and nei[6] != '' else NOT_SET,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET,
                options=options
            )
        )

    return list_vrf
