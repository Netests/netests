#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.vrf import VRF, ListVRF


def _cumulus_vrf_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    cmd_output = parse_textfsm(
        content=cmd_output.decode(),
        template_file='cumulus_net_show_vrf.textfsm'
    )

    list_vrf = ListVRF(list())
    list_vrf.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="1000",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )
    )

    for line in cmd_output:
        list_vrf.vrf_lst.append(VRF(
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
        )

    return list_vrf
