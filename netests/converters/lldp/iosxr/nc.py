#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.protocols.lldp import LLDP, ListLLDP


def _iosxr_lldp_nc_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    cmd_output = format_xml_output(cmd_output)

    return lldp_neighbors_lst
