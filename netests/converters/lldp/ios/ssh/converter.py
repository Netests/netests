#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
from const.constants import NOT_SET, LEVEL1
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_ios_show_lldp_neighbors_detail.textfsm"
    )

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    for nei in cmd_output:
        neighbor_type_lst = list()
        for sys_capability in nei[6]:
            neighbor_type_lst.append(
                _mapping_sys_capabilities(
                    str(sys_capability).capitalize()
                )
            )

        lldp_neighbors_lst.lldp_neighbors_lst.append(
            LLDP(
                local_name=hostname,
                local_port=nei[0] if nei[0] != '' else NOT_SET,
                neighbor_mgmt_ip=nei[7] if nei[7] != '' else NOT_SET,
                neighbor_name=nei[4] if nei[4] != '' else NOT_SET,
                neighbor_port=nei[2] if nei[2] != '' else NOT_SET,
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
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
