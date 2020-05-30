#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.tools.nc import format_xml_output
from netests.protocols.lldp import ListLLDP


def _ios_lldp_nc_converter(
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
        pass

    return lldp_neighbors_lst
