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


def _iosxr_cdp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_xr_show_cdp_neighbors_detail.textfsm"
    )

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    for n in cmd_output:
        capabilities = list()
        for c in n[7].split(" "):
            if _mapping_sys_capabilities(c) != NOT_SET:
                capabilities.append(
                    _mapping_sys_capabilities(c)
                )

        cdp_neighbors_lst.cdp_neighbors_lst.append(
            CDP(
                local_name=hostname,
                local_port=n[5],
                neighbor_mgmt_ip=n[2],
                neighbor_name=n[0],
                neighbor_port=n[4],
                neighbor_os=n[6],
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
        PP.pprint(cdp_neighbors_lst.to_json())

    return cdp_neighbors_lst
