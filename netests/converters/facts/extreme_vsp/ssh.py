#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.tools.cli import parse_textfsm
from netests.constants import (
    NOT_SET,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY
)


def _extreme_vsp_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:
    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_INT_DICT_KEY] = parse_textfsm(
            content=cmd_output[FACTS_INT_DICT_KEY],
            template_file="extrme_vsp_show_int_gi_name.textfsm"
        )
        for i in cmd_output.get(FACTS_INT_DICT_KEY):
            interfaces_lst.append(i[0])

    hostname = NOT_SET
    version = NOT_SET
    model = NOT_SET
    serial = NOT_SET
    base_mac = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_SYS_DICT_KEY] = parse_textfsm(
            content=cmd_output[FACTS_SYS_DICT_KEY],
            template_file="extreme_vsp_show_tech.textfsm"
        )
        for v in cmd_output.get(FACTS_SYS_DICT_KEY):
            hostname = v[1] if v[1] != "" else NOT_SET
            version = v[0] if v[0] != "" else NOT_SET
            model = v[2] if v[2] != "" else NOT_SET
            # vendor = v[3] if v[3] != "" else NOT_SET
            serial = v[4] if v[4] != "" else NOT_SET
            base_mac = v[5] if v[5] != "" else NOT_SET

    domain = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_DOMAIN_DICT_KEY] = parse_textfsm(
            content=cmd_output[FACTS_DOMAIN_DICT_KEY],
            template_file="extreme_vsp_show_sys_dns.textfsm"
        )
        for v in cmd_output.get(FACTS_DOMAIN_DICT_KEY):
            domain = v[0] if v[0] != "" else NOT_SET

    return Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=base_mac,
        memory=NOT_SET,
        vendor="Extreme Networks",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )
