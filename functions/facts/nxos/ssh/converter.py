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


def _nxos_facts_ssh_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:
    if cmd_output is None:
        return dict()

    """
    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:
            sys_info_obj.hostname = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("host_name", NOT_SET)
            sys_info_obj.version = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("kickstart_ver_str", NOT_SET)
            sys_info_obj.serial = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("proc_board_id")
            sys_info_obj.base_mac = NOT_SET
            sys_info_obj.memory = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("memory", NOT_SET)
            sys_info_obj.vendor = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("manufacturer")
            sys_info_obj.model = cmd_outputs.get(
                INFOS_SYS_DICT_KEY).get("chassis_id", NOT_SET)

        elif key == INFOS_SNMP_DICT_KEY:
            if isinstance(cmd_outputs.get(INFOS_SNMP_DICT_KEY)
            .get("TABLE_host", NOT_SET).get("ROW_host"), list):

                for snmp_host in cmd_outputs.get(INFOS_SNMP_DICT_KEY)
                                            .get("TABLE_host")
                                            .get("ROW_host"):

                    sys_info_obj.snmp_ips.append(snmp_host.get("host"))

            elif isinstance(cmd_outputs.get(INFOS_SNMP_DICT_KEY)
            .get("TABLE_host", NOT_SET).get("ROW_host"), dict):
                sys_info_obj.snmp_ips = [cmd_outputs.get(INFOS_SNMP_DICT_KEY)
                    .get("TABLE_host", NOT_SET).get("ROW_host").get("host")]

        elif key == INFOS_INT_DICT_KEY:
            sys_info_obj.interfaces_lst = _nexus_retrieve_int_name(
                cmd_outputs.get(INFOS_INT_DICT_KEY).get(
                    "TABLE_interface", NOT_SET).get("ROW_interface")
            )

        elif key == INFOS_DOMAIN_DICT_KEY:
            if "." in cmd_outputs.get(INFOS_DOMAIN_DICT_KEY)
                                 .get('hostname', NOT_SET):
                index_fqdn = len(
                    str(f"{cmd_outputs.get(INFOS_SYS_DICT_KEY
                        ).get('host_name', NOT_SET)}."))
                sys_info_obj.domain = cmd_outputs.get(INFOS_DOMAIN_DICT_KEY)
                                                 .get("hostname")[index_fqdn:]

    return sys_info_obj
    """


def _nexus_retrieve_int_name(interface_data: list) -> list:
    int_name_lst = list()
    if interface_data is not None:
        for i in interface_data:
            int_name_lst.append(i.get("interface"))
    return int_name_lst
