#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.cdp import CDP, ListCDP
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
) -> ListCDP:
    
    cmd_output = format_xml_output(cmd_output)

    print(cmd_output)

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if (
        'data' in cmd_output.keys() and
        'cdp-neighbor-details' in cmd_output.get('data').keys()
    ):
        print("jhdh")

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(cdp_neighbors_lst.to_json())

    return cdp_neighbors_lst
