#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL5
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_facts_api_converter(
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
        PP.pprint(json.loads(cmd_output))

    hostname = NOT_SET
    domain = NOT_SET
    version = NOT_SET
    model = NOT_SET
    serial = NOT_SET
    interfaces_lst = list()
    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)
    if (
        isinstance(cmd_output, dict) and
        'Cisco-IOS-XE-native:native' in cmd_output.keys()
    ):
        hostname = cmd_output.get('Cisco-IOS-XE-native:native') \
                             .get('hostname')
        domain = cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('ip') \
                           .get('domain') \
                           .get('name')
        version = cmd_output.get('Cisco-IOS-XE-native:native') \
                            .get('version')
        serial = cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('license') \
                           .get('udi') \
                           .get('sn')
        model = cmd_output.get('Cisco-IOS-XE-native:native') \
                          .get('license') \
                          .get('udi') \
                          .get('pid')
        for t in cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('interface').keys():
            for i in cmd_output.get('Cisco-IOS-XE-native:native') \
                               .get('interface') \
                               .get(t):
                interfaces_lst.append(f"{t}{i.get('name')}")

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
