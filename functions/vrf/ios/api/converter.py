#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from functions.global_tools import printline
from functions.netconf_tools import format_xml_output
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL4,
    LEVEL5,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.verbose_mode import (
    verbose_mode
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_vrf_api_converter(hostname: str(), cmd_output: list) -> ListVRF:
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(type(cmd_output))
        print(cmd_output)
    
    cmd_output = format_xml_output(cmd_output)
    
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(type(cmd_output))
        PP.pprint(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())
    vrf_list.vrf_lst.append(
        VRF(
            vrf_name='default',
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    for v in cmd_output.get('native').get('vrf').get('definition'):

        rt_exp = NOT_SET
        rt_imp = NOT_SET
        if 'route-target' in v.keys():
            if 'export' in v.get('route-target').keys():
                rt_exp = v.get('route-target').get('export')
            if 'import' in v.get('route-target').keys():
                rt_imp = v.get('route-target').get('import')

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=v.get('name', NOT_SET),
                vrf_id=NOT_SET,
                vrf_type=NOT_SET,
                l3_vni=NOT_SET,
                rd=v.get('rd', NOT_SET),
                rt_imp=rt_imp,
                rt_exp=rt_exp,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET
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
