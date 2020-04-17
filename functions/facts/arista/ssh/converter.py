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

    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:

            version = cmd_outputs.get(INFOS_SYS_DICT_KEY)
                                 .get("version", NOT_SET)
            build = cmd_outputs.get(INFOS_SYS_DICT_KEY)
                               .get("internalVersion", NOT_SET)
            serial = cmd_outputs.get(INFOS_SYS_DICT_KEY)
                                .get("serialNumber", NOT_SET)
            base_mac = NOT_SET
            memory = cmd_outputs.get(INFOS_SYS_DICT_KEY)
                                .get("memFree", NOT_SET)
            vendor = "Arista"
            model = cmd_outputs.get(INFOS_SYS_DICT_KEY)
                               .get("modelName", NOT_SET)


        elif key == INFOS_INT_DICT_KEY:
            .interfaces_lst = _arista_retrieve_int_name(
                cmd_outputs.get(INFOS_INT_DICT_KEY)
                           .get("interfaceStatuses", list())
            )

        elif key == INFOS_DOMAIN_DICT_KEY:

            hostname = cmd_outputs.get(INFOS_DOMAIN_DICT_KEY)
                                  .get("hostname", NOT_SET)

            index_fqdn = len(
                str(
                    f"{cmd_outputs.get(INFOS_DOMAIN_DICT_KEY)
                                  .get('hostname', NOT_SET)}."
                )
            )

            domain = str(cmd_outputs.get(INFOS_DOMAIN_DICT_KEY)
                                    .get("fqdn", NOT_SET))[index_fqdn:]

    return sys_info_obj
    """


def _arista_retrieve_int_name(interface_data: list) -> list:
    int_name_lst = list()
    if interface_data is None:
        for i in interface_data.keys():
            int_name_lst.append(i)
    return int_name_lst
