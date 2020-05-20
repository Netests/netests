#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.cdp import ListCDP
from netests.constants import NOT_SET


def _nxos_cdp_netconf_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    return cdp_neighbors_lst
