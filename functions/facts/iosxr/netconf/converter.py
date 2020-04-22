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
    LEVEL5
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _iosxr_facts_netconf_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(type(cmd_output))
        print(cmd_output)

    hostname = NOT_SET
    domain = NOT_SET
    version = NOT_SET
    serial = NOT_SET
    model = NOT_SET
    interfaces_lst = list()




    facts = Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=NOT_SET,
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
