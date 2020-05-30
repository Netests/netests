#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.facts import Facts
from netests.constants import NOT_SET, FACTS_SYS_DICT_KEY, FACTS_INT_DICT_KEY


def _cumulus_facts_api_converter(
    hostname: str,
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
    build = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        cmd_output[FACTS_SYS_DICT_KEY] = json.loads(
            cmd_output.get(FACTS_SYS_DICT_KEY)
        )

        if '\\n' in cmd_output.get(FACTS_SYS_DICT_KEY) \
                              .get("hostname", NOT_SET):
            i = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get("hostname", NOT_SET).find("\n")
            hostname = cmd_output.get(FACTS_SYS_DICT_KEY) \
                                 .get("hostname", NOT_SET)[:(i-1)]
        elif '\n' in cmd_output.get(FACTS_SYS_DICT_KEY) \
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
        build = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get("build", NOT_SET)
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
        cmd_output[FACTS_INT_DICT_KEY] = json.loads(
            cmd_output.get(FACTS_INT_DICT_KEY)
        )
        for interface_name in cmd_output.get(FACTS_INT_DICT_KEY).keys():
            if "swp" in interface_name or "eth" in interface_name:
                interfaces_lst.append(interface_name)

    return Facts(
        hostname=hostname,
        domain=NOT_SET,
        version=version,
        build=build,
        serial=serial,
        base_mac=base_mac,
        memory=memory,
        vendor=vendor,
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )
