#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.facts import Facts
from netests.constants import (
    NOT_SET,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY
)


def _nxos_facts_ssh_converter(
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
        if not isinstance(cmd_output.get(FACTS_SYS_DICT_KEY), dict):
            cmd_output[FACTS_SYS_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_SYS_DICT_KEY)
            )
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
        if not isinstance(cmd_output.get(FACTS_DOMAIN_DICT_KEY), dict):
            cmd_output[FACTS_DOMAIN_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_DOMAIN_DICT_KEY)
            )
        if "." in cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                            .get('hostname', NOT_SET):
            i = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                          .get('hostname', NOT_SET).find('.')
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get("hostname")[i+1:]
        else:
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get("hostname")

    return Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=memory,
        vendor="Cisco" if True else vendor,
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )


def _nexus_retrieve_int_name(interface_data: list) -> list:
    int_name_lst = list()
    if interface_data is not None:
        for i in interface_data:
            int_name_lst.append(i.get("interface"))
    return int_name_lst
