#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.mappings import mapping_interface_name
from netests.constants import (
    NOT_SET,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_MEMORY_DICT_KEY,
    FACTS_CONFIG_DICT_KEY,
    FACTS_SERIAL_DICT_KEY
)


def _juniper_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:
    if cmd_output is None:
        return dict()

    interface_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        for i in cmd_output.get(FACTS_INT_DICT_KEY) \
                           .get('interface-information')[0] \
                           .get('physical-interface'):
            interface_lst.append(i.get('name')[0].get('data'))

    memory = NOT_SET
    if FACTS_MEMORY_DICT_KEY in cmd_output.keys():
        memory = cmd_output.get(FACTS_MEMORY_DICT_KEY) \
                           .get("system-memory-information")[0] \
                           .get("system-memory-summary-information")[0] \
                           .get("system-memory-total")[0] \
                           .get("data", NOT_SET)

    hostname = NOT_SET
    domain = NOT_SET
    if FACTS_CONFIG_DICT_KEY in cmd_output.keys():
        hostname = cmd_output.get(FACTS_CONFIG_DICT_KEY) \
                              .get("configuration") \
                              .get("system") \
                              .get("host-name", NOT_SET)
        domain = cmd_output.get(FACTS_CONFIG_DICT_KEY) \
                           .get("configuration") \
                           .get("system") \
                           .get("domain-name", NOT_SET)

    model = NOT_SET
    version = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        model = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get('software-information')[0] \
                          .get('product-model')[0] \
                          .get('data', NOT_SET).upper()
        version = cmd_output.get(FACTS_SYS_DICT_KEY) \
                            .get('software-information')[0] \
                            .get('junos-version')[0] \
                            .get('data', NOT_SET)

    serial = NOT_SET
    if FACTS_SERIAL_DICT_KEY in cmd_output.keys():
        serial = cmd_output.get(FACTS_SERIAL_DICT_KEY) \
                           .get("chassis-inventory")[0] \
                           .get("chassis")[0] \
                           .get("serial-number")[0] \
                           .get("data", NOT_SET)

    return Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=memory,
        vendor="Juniper",
        model=model,
        interfaces_lst=interface_lst,
        options=options
    )


def _juniper_retrieve_int_name(interface_data: dict) -> list:

    int_name_lst = list()

    for interface_name in interface_data:
        if (
            (
                "em" in interface_name.get("name")[0].get("data") or
                "lo" in interface_name.get("name")[0].get("data") or
                "fxp" in interface_name.get("name")[0].get("data")
            ) and
            "demux" not in interface_name.get("name")[0].get("data") and
            "local" not in interface_name.get("name")[0].get("data") and
            interface_name.get("name")[0].get("data", NOT_SET) != NOT_SET
        ):
            int_name_lst.append(
                mapping_interface_name(
                    interface_name.get("name")[0].get("data"))
            )

    return int_name_lst
