#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.cdp import CDP, ListCDP
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
from const.constants import NOT_SET, LEVEL1
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

    for nei in cmd_output:
        neighbor_type_lst = list()

        if isinstance(nei[6], list):
            for sys_capability in nei[6]:
                print(">>", sys_capability)
                neighbor_type_lst.append(
                    _mapping_sys_capabilities(
                       str(sys_capability).capitalize()
                    )
                )
        else:
            neighbor_type_lst.append(nei[6])

        cdp_neighbors_lst.cdp_neighbors_lst.append(
            CDP(
                local_name=hostname,
                local_port=nei[4] if nei[4] != '' else NOT_SET,
                neighbor_mgmt_ip=nei[1] if nei[1] != '' else NOT_SET,
                neighbor_name=nei[0] if nei[0] != '' else NOT_SET,
                neighbor_port=nei[3] if nei[3] != '' else NOT_SET,
                neighbor_os=nei[5] if nei[5] != '' else NOT_SET,
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
