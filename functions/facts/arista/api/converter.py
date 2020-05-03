#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.discovery_protocols.discovery_functions import (
    _mapping_interface_name
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_facts_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    if 'result' in cmd_output.keys():
        if not isinstance(cmd_output.get('result')[1], dict):
            cmd_output.get('result')[1] = json.loads(
                cmd_output.get('result')[1]
            )
        for interface_name in cmd_output.get('result')[1] \
                                        .get('interfaceStatuses'):
            if "Eth" in interface_name or "Mana" in interface_name:
                interfaces_lst.append(interface_name)

    version = NOT_SET
    serial = NOT_SET
    base_mac = NOT_SET
    memory = NOT_SET
    model = NOT_SET
    build = NOT_SET
    if 'result' in cmd_output.keys():
        if not isinstance(cmd_output.get('result')[1], dict):
            cmd_output.get('result')[0] = json.loads(
                cmd_output.get('result')[0]
            )
        memory = cmd_output.get('result')[0].get('memTotal')
        model = cmd_output.get('result')[0].get('modelName')
        version = cmd_output.get('result')[0].get('version')
        serial = cmd_output.get('result')[0].get('serialNumber')
        base_mac = cmd_output.get('result')[0].get('systemMacAddress')
        build = cmd_output.get('result')[0].get('internalBuildId')


    if 'result' in cmd_output.keys():
        if not isinstance(cmd_output.get('result')[2], dict):
            cmd_output.get('result')[2] = json.loads(
                cmd_output.get('result')[2]
            )
        hostname = cmd_output.get('result')[2].get('hostname')
        if "." in cmd_output.get('result')[2].get('fqdn'):
            i = cmd_output.get('result')[2] \
                          .get('fqdn', NOT_SET).find('.')
            domain = cmd_output.get('result')[2] \
                               .get("fqdn")[i+1:]
        else:
            domain = cmd_output.get('result')[2].get("fqdn")

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
