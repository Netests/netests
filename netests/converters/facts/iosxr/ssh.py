#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.tools.cli import parse_textfsm
from netests.constants import NOT_SET, FACTS_SYS_DICT_KEY, FACTS_INT_DICT_KEY


def _iosxr_facts_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_INT_DICT_KEY] = parse_textfsm(
            content=cmd_output.get(FACTS_INT_DICT_KEY),
            template_file='cisco_xr_show_ip_interface_brief.textfsm'
        )
        for i in cmd_output.get(FACTS_INT_DICT_KEY):
            interfaces_lst.append(i[0])

    hostname = NOT_SET
    version = NOT_SET
    model = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_SYS_DICT_KEY] = parse_textfsm(
            content=cmd_output.get(FACTS_SYS_DICT_KEY),
            template_file='cisco_xr_show_version.textfsm'
        )
        for i in cmd_output.get(FACTS_SYS_DICT_KEY):
            hostname = i[4] if i[4] != "" else NOT_SET
            version = i[0] if i[0] != "" else NOT_SET
            model = i[3] if i[3] != "" else NOT_SET

    return Facts(
        hostname=hostname,
        domain=NOT_SET,
        version=version,
        build=NOT_SET,
        serial=NOT_SET,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor="Cisco",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )
