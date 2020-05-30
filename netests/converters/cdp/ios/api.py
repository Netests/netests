#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.cdp import ListCDP


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

    return cdp_neighbors_lst
