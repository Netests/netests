#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL1, LEVEL3
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_cdp_netconf_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:
    
    cmd_output = format_xml_output(cmd_output)

    print(cmd_output)

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if (
        'data' in cmd_output.keys() and
        'lldp-entries' in cmd_output.get('data').keys()
    ):
        print("jhdh")

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
