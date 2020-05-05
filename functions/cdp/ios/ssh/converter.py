#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.cdp import CDP, ListCDP
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
from const.constants import NOT_SET, LEVEL1, LEVEL3
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_cdp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_ios_show_cdp_neighbors_detail.textfsm"
    )

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    for l in cmd_output:
        neighbor_type_lst = list()
        
        if isinstance(l[6], list):
            for sys_capability in l[6]:
                print(">>", sys_capability)
                neighbor_type_lst.append(
                    _mapping_sys_capabilities(
                       str(sys_capability).capitalize()
                    )
                )
        else:
            neighbor_type_lst.append(l[6])
        
        cdp_neighbors_lst.cdp_neighbors_lst.append(
            CDP(
                local_name=hostname,
                local_port=l[4] if l[4] is not '' else NOT_SET,
                neighbor_mgmt_ip=l[1] if l[1] is not '' else NOT_SET,
                neighbor_name=l[0] if l[0] is not '' else NOT_SET,
                neighbor_port=l[3] if l[3] is not '' else NOT_SET,
                neighbor_os=l[5] if l[5] is not '' else NOT_SET,
                neighbor_type=neighbor_type_lst,
                options=options
            )
        )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(cdp_neighbors_lst.to_json())

    return cdp_neighbors_lst
