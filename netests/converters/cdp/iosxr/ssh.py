#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.cdp import CDP, ListCDP
from netests.mappings import mapping_sys_capabilities


def _iosxr_cdp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_xr_show_cdp_neighbors_detail.textfsm"
    )

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    for n in cmd_output:
        capabilities = list()
        for c in n[7].split(" "):
            if mapping_sys_capabilities(c) != NOT_SET:
                capabilities.append(
                    mapping_sys_capabilities(c)
                )

        cdp_neighbors_lst.cdp_neighbors_lst.append(
            CDP(
                local_name=hostname,
                local_port=n[5],
                neighbor_mgmt_ip=n[2],
                neighbor_name=n[0],
                neighbor_port=n[4],
                neighbor_os=n[6],
                neighbor_type=capabilities,
                options=options
            )
        )

    return cdp_neighbors_lst
