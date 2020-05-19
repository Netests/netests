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


def _iosxr_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_xr_show_lldp_neighbors.textfsm"
    )

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    for nei in cmd_output:
        capabilities = list()
        for c in nei[3]:
            if c.isdigit():
                capabilities.append(
                    _mapping_sys_capabilities(c)
                )

        lldp_neighbors_lst.lldp_neighbors_lst.append(
            LLDP(
                local_name=hostname,
                local_port=nei[1] if nei[1] != '' else NOT_SET,
                neighbor_mgmt_ip=NOT_SET,
                neighbor_name=nei[0] if nei[0] != '' else NOT_SET,
                neighbor_port=nei[2] if nei[2] != '' else NOT_SET,
                neighbor_os=NOT_SET,
                neighbor_type=capabilities,
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
