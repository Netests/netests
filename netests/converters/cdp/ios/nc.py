#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.tools.nc import format_xml_output
from netests.protocols.cdp import ListCDP


def _ios_cdp_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cmd_output = format_xml_output(cmd_output)

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if (
        'data' in cmd_output.keys() and
        'cdp-neighbor-details' in cmd_output.get('data').keys()
    ):
        pass

    return cdp_neighbors_lst
