#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.tools.nc import format_xml_output
from netests.constants import NOT_SET, FACTS_INT_DICT_KEY, FACTS_SYS_DICT_KEY


def _juniper_facts_nc_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    interfaces_lst = list()
    for i in format_xml_output(
        cmd_output.get(FACTS_INT_DICT_KEY)
    ).get('interface-information').get('physical-interface'):
        interfaces_lst.append(i.get('name'))

    return Facts(
        hostname=cmd_output.get(FACTS_SYS_DICT_KEY).get('hostname', NOT_SET),
        domain=cmd_output.get(FACTS_SYS_DICT_KEY).get('domain', NOT_SET),
        build=NOT_SET,
        version=cmd_output.get(FACTS_SYS_DICT_KEY).get('version', NOT_SET),
        serial=cmd_output.get(FACTS_SYS_DICT_KEY).get('serialnumber', NOT_SET),
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor="Juniper",
        model=cmd_output.get(FACTS_SYS_DICT_KEY).get('model', NOT_SET).upper(),
        interfaces_lst=interfaces_lst,
        options=options
    )
