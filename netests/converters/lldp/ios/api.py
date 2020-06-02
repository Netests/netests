#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.lldp import ListLLDP


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
