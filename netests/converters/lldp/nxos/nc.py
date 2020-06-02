#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.lldp import ListLLDP


def _nxos_lldp_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    return lldp_neighbors_lst
