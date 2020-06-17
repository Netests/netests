#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.tools.cli import parse_textfsm
from netests.protocols.vlan import ListVLAN


def _ios_vlan_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListVLAN:

    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    cmd_output = parse_textfsm(
        content=cmd_output,
        template_file='cisco_ios_show_vlan.textfsm'
    )

    print(cmd_output)

    return vlan_lst
