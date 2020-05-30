#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.lldp import LLDP, ListLLDP


def _ios_lldp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    print(cmd_output)

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    return lldp_neighbors_lst
