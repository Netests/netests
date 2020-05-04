#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.cli_tools import parse_textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_facts_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_INT_DICT_KEY] = parse_textfsm(
            content=cmd_output.get(FACTS_INT_DICT_KEY),
            template_file='cisco_ios_show_ip_int_brief.textfsm'
        )
        for i in cmd_output.get(FACTS_INT_DICT_KEY):
            interfaces_lst.append(i[0])

    hostname = NOT_SET
    version = NOT_SET
    model = NOT_SET
    serial = NOT_SET
    build = NOT_SET
    memory = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_SYS_DICT_KEY] = parse_textfsm(
            content=cmd_output.get(FACTS_SYS_DICT_KEY),
            template_file='cisco_ios_show_version.textfsm'
        )
        for i in cmd_output.get(FACTS_SYS_DICT_KEY):
            hostname = i[2] if i[2] != "" else NOT_SET
            version = i[0] if i[0] != "" else NOT_SET
            model = i[10] if i[10] != "" else NOT_SET
            serial = i[7][0] if i[7][0] != "" else NOT_SET
            build = i[11] if i[11] != "" else NOT_SET
            memory = i[12] if i[12] != "" else NOT_SET

    facts = Facts(
        hostname=hostname,
        domain=NOT_SET,
        version=version,
        build=build,
        serial=serial,
        base_mac=NOT_SET,
        memory=memory,
        vendor="Cisco",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        PP.pprint(facts.to_json())

    return facts
