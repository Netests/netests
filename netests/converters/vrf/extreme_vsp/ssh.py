#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.vrf import VRF, ListVRF


def _extreme_vsp_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file='extreme_vsp_show_ip_vrf.textfsm'
    )

    vrf_list = ListVRF(list())

    for vrf in cmd_output:
        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf[0],
                vrf_id=vrf[1],
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=NOT_SET,
                rt_imp=NOT_SET,
                rt_exp=NOT_SET,
                exp_targ=NOT_SET,
                imp_targ=NOT_SET,
                options=options
            )
        )

    return vrf_list


def _extreme_vsp_vrf_mapping(vrf_name: str) -> str:
    """
    This function will convert Extreme Networks VSP
    routing instance (GlobalRouter & MgmtRouter)
    => GlobalRouter => default
    => MgmtRouter => mgmt

    * Return :
        1) "default" if vrf_name = "GlobalRouter"
        2) "mgmt" if vrf_name = "MgmtRouter"
        3) else vrf_name

    :param vrf_name:
    :return str:
    """
    if vrf_name == "GlobalRouter":
        return "default"
    elif vrf_name == "MgmtRouter":
        return "mgmt"
    else:
        return vrf_name
