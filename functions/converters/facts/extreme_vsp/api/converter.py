#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _extreme_vsp_facts_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    hostname = NOT_SET
    domain = NOT_SET
    memory = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        hostname = cmd_output.get(FACTS_SYS_DICT_KEY) \
                             .get('openconfig-system:system') \
                             .get('config') \
                             .get('hostname', NOT_SET)
        domain = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get('openconfig-system:system') \
                           .get('config') \
                           .get('domain-name', NOT_SET)

        memory = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get('openconfig-system:system') \
                           .get('memory') \
                           .get('state') \
                           .get('physical', NOT_SET)

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        for i in cmd_output.get(FACTS_INT_DICT_KEY) \
                           .get('openconfig-interfaces:interfaces') \
                           .get('interface'):
            interfaces_lst.append(i.get('name'))

    facts = Facts(
        hostname=hostname,
        domain=domain,
        version=NOT_SET,
        build=NOT_SET,
        serial=NOT_SET,
        base_mac=NOT_SET,
        memory=memory,
        vendor="Extreme Networks",
        model=NOT_SET,
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
