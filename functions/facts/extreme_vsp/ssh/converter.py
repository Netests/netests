#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import os
from protocols.facts import Facts
"""
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
    FACTS_MEMORY_DICT_KEY,
    FACTS_CONFIG_DICT_KEY,
    FACTS_SERIAL_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)
"""


def _arista_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:
    if cmd_output is None:
        return dict()

    """
    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key in cmd_outputs.keys():
        if key == INFOS_SYS_DICT_KEY:

            for value in cmd_outputs.get(INFOS_SYS_DICT_KEY):
                version = value[0] if value[0] != "" else NOT_SET
                hostname = value[1] if value[1] != "" else NOT_SET
                model = value[2] if value[2] != "" else NOT_SET
                vendor = value[3] if value[3] != "" else NOT_SET
                serial = value[4] if value[4] != "" else NOT_SET
                base_mac = value[5] if value[5] != ""

        if key == INFOS_DOMAIN_DICT_KEY:

            for value in cmd_outputs.get(INFOS_DOMAIN_DICT_KEY):

                sys_info_obj.domain = value[0] if value[0] != "" else NOT_SET

        if key == INFOS_SNMP_DICT_KEY:

            for value in cmd_outputs.get(INFOS_SNMP_DICT_KEY):

                sys_info_obj.snmp_ips.append(value[0])

        if key == INFOS_INT_DICT_KEY:

            for value in cmd_outputs.get(INFOS_INT_DICT_KEY):

                sys_info_obj.interfaces_lst.append(
                    _mapping_interface_name(value[0])
                )

    return sys_info_obj
    """
