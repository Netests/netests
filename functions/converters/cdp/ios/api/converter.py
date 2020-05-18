#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.cdp import ListCDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_cdp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    if not isinstance(cmd_output, dict):
        if isinstance(cmd_output, bytes):
            if cmd_output.decode() != "":
                cmd_output = json.loads(cmd_output)
        else:
            cmd_output = json.loads(cmd_output)

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(cdp_neighbors_lst.to_json())

    return cdp_neighbors_lst
