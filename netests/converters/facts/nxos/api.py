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


def _nxos_facts_api_converter(
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
                           .get('ins_api') \
                           .get('outputs') \
                           .get('output') \
                           .get('body') \
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
                             .get('ins_api') \
                             .get('outputs') \
                             .get('output') \
                             .get('body') \
                             .get('host_name')
        version = cmd_output.get(FACTS_SYS_DICT_KEY) \
                            .get('ins_api') \
                            .get('outputs') \
                            .get('output') \
                            .get('body') \
                            .get("kickstart_ver_str", NOT_SET)
        serial = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get('ins_api') \
                           .get('outputs') \
                           .get('output') \
                           .get('body') \
                           .get("proc_board_id", NOT_SET)
        memory = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get('ins_api') \
                           .get('outputs') \
                           .get('output') \
                           .get('body') \
                           .get("memory", NOT_SET)
        vendor = cmd_output.get(FACTS_SYS_DICT_KEY) \
                           .get('ins_api') \
                           .get('outputs') \
                           .get('output') \
                           .get('body') \
                           .get("manufacturer", NOT_SET)
        model = cmd_output.get(FACTS_SYS_DICT_KEY) \
                          .get('ins_api') \
                          .get('outputs') \
                          .get('output') \
                          .get('body') \
                          .get("chassis_id", NOT_SET)

    domain = NOT_SET
    if FACTS_DOMAIN_DICT_KEY in cmd_output.keys():
        if not isinstance(cmd_output.get(FACTS_DOMAIN_DICT_KEY), dict):
            cmd_output[FACTS_DOMAIN_DICT_KEY] = json.loads(
                cmd_output.get(FACTS_DOMAIN_DICT_KEY)
            )
        if "." in cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                            .get('ins_api') \
                            .get('outputs') \
                            .get('output') \
                            .get('body') \
                            .get('hostname', NOT_SET):
            i = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                          .get('ins_api') \
                          .get('outputs') \
                          .get('output') \
                          .get('body') \
                          .get('hostname', NOT_SET).find('.')
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get('ins_api') \
                               .get('outputs') \
                               .get('output') \
                               .get('body') \
                               .get("hostname")[i+1:]
        else:
            domain = cmd_output.get(FACTS_DOMAIN_DICT_KEY) \
                               .get('ins_api') \
                               .get('outputs') \
                               .get('output') \
                               .get('body') \
                               .get('hostname', NOT_SET)

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
