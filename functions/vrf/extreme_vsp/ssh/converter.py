#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
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


def _extreme_vsp_vrf_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:
    template = open(
        f"{TEXTFSM_PATH}extreme_vsp_show_ip_vrf.textfsm")
    results_template = textfsm.TextFSM(template)
    parsed_results = results_template.ParseText(cmd_output)

    vrf_list = ListVRF(list())

    for vrf in parsed_results:
        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=_extreme_vsp_vrf_mapping(vrf[0]),
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
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

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
