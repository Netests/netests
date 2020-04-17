#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL5,
    FACTS_INT_DICT_KEY,
    FACTS_SYS_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_facts_netconf_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        PP.pprint(cmd_output)

    interfaces_lst = list()
    for i in format_xml_output(
        cmd_output.get(FACTS_INT_DICT_KEY)
    ).get('interface-information').get('physical-interface'):
        interfaces_lst.append(i.get('name'))

    facts = Facts(
        hostname=cmd_output.get(FACTS_SYS_DICT_KEY).get('hostname', NOT_SET),
        domain=cmd_output.get(FACTS_SYS_DICT_KEY).get('domain', NOT_SET),
        build=NOT_SET,
        version=cmd_output.get(FACTS_SYS_DICT_KEY).get('version', NOT_SET),
        serial=cmd_output.get(FACTS_SYS_DICT_KEY).get('serialnumber', NOT_SET),
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor="Juniper",
        model=cmd_output.get(FACTS_SYS_DICT_KEY).get('model', NOT_SET),
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
