#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.cli_tools import parse_textfsm
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1, LEVEL3
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _extreme_vsp_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    v = parse_textfsm(
        content=cmd_output,
        template_file='extreme_vsp_show_lldp_neighbor.textfsm'
    )

    for l in v:
        neighbor_type_lst = list()
        for sys_capability in l[4]:
            neighbor_type_lst.append(
                _mapping_sys_capabilities(
                    str(sys_capability).capitalize()
                )
            )

        lldp_neighbors_lst.lldp_neighbors_lst.append(
            LLDP(
                local_name=hostname,
                local_port=l[0],
                neighbor_mgmt_ip=l[7],
                neighbor_name=l[3],
                neighbor_port=l[2],
                neighbor_os=l[6],
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


