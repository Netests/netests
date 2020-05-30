#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.cdp import CDP, ListCDP
from netests.mappings import mapping_sys_capabilities


def _ios_cdp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_ios_show_cdp_neighbors_detail.textfsm"
    )

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    for nei in cmd_output:
        neighbor_type_lst = list()

        if isinstance(nei[6], list):
            for sys_capability in nei[6]:
                neighbor_type_lst.append(
                    mapping_sys_capabilities(
                       str(sys_capability).capitalize()
                    )
                )
        else:
            neighbor_type_lst.append(nei[6])

        cdp_neighbors_lst.cdp_neighbors_lst.append(
            CDP(
                local_name=hostname,
                local_port=nei[4] if nei[4] != '' else NOT_SET,
                neighbor_mgmt_ip=nei[1] if nei[1] != '' else NOT_SET,
                neighbor_name=nei[0] if nei[0] != '' else NOT_SET,
                neighbor_port=nei[3] if nei[3] != '' else NOT_SET,
                neighbor_os=nei[5] if nei[5] != '' else NOT_SET,
                neighbor_type=neighbor_type_lst,
                options=options
            )
        )

    return cdp_neighbors_lst
