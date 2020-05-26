#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.tools.nc import format_xml_output
from netests.constants import (
    NOT_SET,
    FACTS_INT_DICT_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_SERIAL_DICT_KEY,
    FACTS_MEMORY_DICT_KEY
)


def _juniper_facts_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    if FACTS_INT_DICT_KEY in cmd_output.keys():
        for i in format_xml_output(
            cmd_output.get(FACTS_INT_DICT_KEY)
        ).get('interface-information').get('physical-interface'):
            interfaces_lst.append(i.get('name'))

    hostname = NOT_SET
    version = NOT_SET
    model = NOT_SET
    if FACTS_SYS_DICT_KEY in cmd_output.keys():
        i = format_xml_output(cmd_output.get(FACTS_SYS_DICT_KEY))
        hostname = i.get('software-information') \
                    .get('host-name', NOT_SET)
        version = i.get('software-information') \
                   .get('junos-version', NOT_SET)
        model = i.get('software-information') \
                 .get('product-name', NOT_SET).upper()

    serial = NOT_SET
    if FACTS_SERIAL_DICT_KEY in cmd_output.keys():
        i = format_xml_output(cmd_output.get(FACTS_SERIAL_DICT_KEY))
        serial = i.get('chassis-inventory') \
                  .get('chassis') \
                  .get('serial-number', NOT_SET)

    memory = NOT_SET
    if FACTS_MEMORY_DICT_KEY in cmd_output.keys():
        i = format_xml_output(cmd_output.get(FACTS_MEMORY_DICT_KEY))
        memory = i.get('system-memory-information') \
                  .get('system-memory-summary-information') \
                  .get('system-memory-total', NOT_SET)

    return Facts(
        hostname=hostname,
        domain=NOT_SET,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=memory,
        vendor="Juniper",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options,
    )
