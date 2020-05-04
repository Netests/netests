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
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        if not isinstance(cmd_output.get(FACTS_INT_DICT_KEY), dict):
            cmd_output[FACTS_INT_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_INT_DICT_KEY)
            )
        for interface_name in cmd_output.get(FACTS_INT_DICT_KEY) \
                                        .get('interfaceStatuses') \
                                        .keys():
            if "Eth" in interface_name or "Mana" in interface_name:
                interfaces_lst.append(interface_name)

    version = NOT_SET
    serial = NOT_SET
    base_mac = NOT_SET
    memory = NOT_SET
    model = NOT_SET
    build = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        if not isinstance(cmd_output.get(FACTS_SYS_DICT_KEY), dict):
            cmd_output[FACTS_SYS_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_SYS_DICT_KEY)
            )
        memory = cmd_output.get(FACTS_SYS_DICT_KEY).get('memTotal')
        model = cmd_output.get(FACTS_SYS_DICT_KEY).get('modelName')
        version = cmd_output.get(FACTS_SYS_DICT_KEY).get('version')
        serial = cmd_output.get(FACTS_SYS_DICT_KEY).get('serialNumber')
        base_mac = cmd_output.get(FACTS_SYS_DICT_KEY).get('systemMacAddress')
        build = cmd_output.get(FACTS_SYS_DICT_KEY).get('internalBuildId')

    hostname = NOT_SET
    domain = NOT_SET
    if FACTS_DOMAIN_DICT_KEY in cmd_output.keys():
        if not isinstance(cmd_output.get(FACTS_DOMAIN_DICT_KEY), dict):
            cmd_output[FACTS_DOMAIN_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_DOMAIN_DICT_KEY)
            )
        hostname = cmd_output.get(FACTS_DOMAIN_DICT_KEY).get('hostname')
        if "." in cmd_output.get(FACTS_DOMAIN_DICT_KEY).get('fqdn'):
            i = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                          .get('fqdn', NOT_SET).find('.')
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get("fqdn")[i+1:]
        else:
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY).get("fqdn")

    facts = Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=build,
        serial=serial,
        base_mac=base_mac,
        memory=memory,
        vendor="Arista",
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
