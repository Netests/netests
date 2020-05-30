#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.lldp import LLDP, ListLLDP
from netests.mappings import mapping_sys_capabilities


def _ios_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file="cisco_ios_show_lldp_neighbors_detail.textfsm"
    )

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    for nei in cmd_output:
        neighbor_type_lst = list()
        for sys_capability in nei[6]:
            neighbor_type_lst.append(
                mapping_sys_capabilities(
                    str(sys_capability).capitalize()
                )
            )

        lldp_neighbors_lst.lldp_neighbors_lst.append(
            LLDP(
                local_name=hostname,
                local_port=nei[0] if nei[0] != '' else NOT_SET,
                neighbor_mgmt_ip=nei[7] if nei[7] != '' else NOT_SET,
                neighbor_name=nei[4] if nei[4] != '' else NOT_SET,
                neighbor_port=nei[2] if nei[2] != '' else NOT_SET,
                neighbor_os=nei[5] if nei[5] != '' else NOT_SET,
                neighbor_type=neighbor_type_lst,
                options=options
            )
        )

    return lldp_neighbors_lst
