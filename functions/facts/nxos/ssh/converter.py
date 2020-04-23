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
    LEVEL5,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_facts_ssh_converter(
    hostname: str(),
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

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        for i in cmd_output.get(FACTS_INT_DICT_KEY) \
                           .get('TABLE_interface') \
                           .get('ROW_interface'):
            interfaces_lst.append(i.get('interface'))

    hostname = NOT_SET
    version = NOT_SET
    serial = NOT_SET
    memory = NOT_SET
    vendor = NOT_SET
    model = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        hostname = cmd_output.get(FACTS_SYS_DICT_KEY) \
                             .get("host_name", NOT_SET)
        version = cmd_output.get(FACTS_SYS_DICT_KEY) \
                            .get("kickstart_ver_str", NOT_SET)
        serial = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("proc_board_id", NOT_SET)
        memory = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("memory", NOT_SET)
        vendor = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("manufacturer", NOT_SET)
        model = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get("chassis_id", NOT_SET)

    domain = NOT_SET
    if FACTS_DOMAIN_DICT_KEY in cmd_output.keys():
        if "." in cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                            .get('hostname', NOT_SET):
            i = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                          .get('hostname', NOT_SET).find('.')
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get("hostname")[i+1:]
        else:
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get("hostname")

    facts = Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
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


def _nexus_retrieve_int_name(interface_data: list) -> list:
    int_name_lst = list()
    if interface_data is not None:
        for i in interface_data:
            int_name_lst.append(i.get("interface"))
    return int_name_lst
