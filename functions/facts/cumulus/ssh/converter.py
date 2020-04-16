#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import lxml
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_MEMORY_DICT_KEY,
    FACTS_CONFIG_DICT_KEY,
    FACTS_SERIAL_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _cumulus_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    hostname = NOT_SET
    version = NOT_SET
    serial = NOT_SET
    base_mac = NOT_SET
    memory = NOT_SET
    vendor = NOT_SET
    model = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        if "\n" in cmd_output.get(FACTS_SYS_DICT_KEY) \
                             .get("hostname", NOT_SET):
            i = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get("hostname", NOT_SET).find("\n")
            hostname = cmd_output.get(FACTS_SYS_DICT_KEY) \
                                 .get("hostname", NOT_SET)[:i]
        else:
            hostname = cmd_output.get(FACTS_SYS_DICT_KEY) \
                                 .get("hostname", NOT_SET)
        version = cmd_output.get(FACTS_SYS_DICT_KEY) \
                            .get("os-version", NOT_SET)
        serial = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("eeprom") \
                           .get("tlv") \
                           .get("Serial Number") \
                           .get("value", NOT_SET)
        base_mac = cmd_output.get(FACTS_SYS_DICT_KEY) \
                             .get("eeprom") \
                             .get("tlv") \
                             .get("Base MAC Address") \
                             .get("value", NOT_SET)
        memory = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("memory", NOT_SET)
        vendor = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get("eeprom") \
                           .get("tlv") \
                           .get("Vendor Name") \
                           .get("value", NOT_SET)
        model = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get("platform") \
                          .get("model", NOT_SET)

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        for interface_name in cmd_output.get(FACTS_INT_DICT_KEY).keys():
            if "swp" in interface_name or "eth" in interface_name:
                interfaces_lst.append(interface_name)

    facts = Facts(
        hostname=hostname,
        domain=NOT_SET,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=base_mac,
        memory=memory,
        vendor=vendor,
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
