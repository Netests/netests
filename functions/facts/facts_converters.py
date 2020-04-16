#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import *
from protocols.infos import SystemInfos
from functions.discovery_protocols.discovery_functions import _mapping_interface_name
import json


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus System Informations Converter
#
def _nexus_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:
            sys_info_obj.hostname = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("host_name", NOT_SET)
            sys_info_obj.version = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("kickstart_ver_str", NOT_SET)
            sys_info_obj.serial = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("proc_board_id")
            sys_info_obj.base_mac = NOT_SET
            sys_info_obj.memory = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("memory", NOT_SET)
            sys_info_obj.vendor = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("manufacturer")
            sys_info_obj.model = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("chassis_id", NOT_SET)

        elif key == INFOS_SNMP_DICT_KEY:
            if isinstance(cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("TABLE_host", NOT_SET).get("ROW_host"), list):

                for snmp_host in cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("TABLE_host", NOT_SET).get("ROW_host"):
                    sys_info_obj.snmp_ips.append(snmp_host.get("host"))

            elif isinstance(cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("TABLE_host", NOT_SET).get("ROW_host"), dict):
                sys_info_obj.snmp_ips = [cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("TABLE_host", NOT_SET).get("ROW_host").get("host")]

        elif key == INFOS_INT_DICT_KEY:
            sys_info_obj.interfaces_lst = _nexus_retrieve_int_name(
                cmd_outputs.get(INFOS_INT_DICT_KEY).get("TABLE_interface", NOT_SET).get("ROW_interface")
            )

        elif key == INFOS_DOMAIN_DICT_KEY:
            if "." in cmd_outputs.get(INFOS_DOMAIN_DICT_KEY).get('hostname', NOT_SET):
                index_fqdn = len(str(f"{cmd_outputs.get(INFOS_SYS_DICT_KEY).get('host_name', NOT_SET)}."))
                sys_info_obj.domain = cmd_outputs.get(INFOS_DOMAIN_DICT_KEY).get("hostname", NOT_SET)[index_fqdn:]

    return sys_info_obj

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus interface filter
#
def _nexus_retrieve_int_name(interface_data:list) -> list:

    int_name_lst = list()

    if interface_data != None:
        for intferce_name in interface_data:
            int_name_lst.append(intferce_name.get("interface"))

    return int_name_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista System Informations Converter
#
def _arista_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:

            sys_info_obj.version = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("version", NOT_SET)
            sys_info_obj.build = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("internalVersion", NOT_SET)
            sys_info_obj.serial = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("serialNumber", NOT_SET)
            sys_info_obj.base_mac = NOT_SET
            sys_info_obj.memory = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("memFree", NOT_SET)
            sys_info_obj.vendor = "Arista"
            sys_info_obj.model = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("modelName", NOT_SET)

        elif key == INFOS_SNMP_DICT_KEY:
            sys_info_obj.snmp_ips = cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("ListeningIPAddresses", NOT_SET)

        elif key == INFOS_INT_DICT_KEY:
            sys_info_obj.interfaces_lst = _arista_retrieve_int_name(
                cmd_outputs.get(INFOS_INT_DICT_KEY).get("interfaceStatuses", list())
            )

        elif key == INFOS_DOMAIN_DICT_KEY:

            sys_info_obj.hostname = cmd_outputs.get(INFOS_DOMAIN_DICT_KEY).get("hostname", NOT_SET)

            index_fqdn = len(str(f"{cmd_outputs.get(INFOS_DOMAIN_DICT_KEY).get('hostname', NOT_SET)}."))

            sys_info_obj.domain = str(cmd_outputs.get(INFOS_DOMAIN_DICT_KEY).get("fqdn", NOT_SET))[index_fqdn:]

    return sys_info_obj

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista interface filter
#
def _arista_retrieve_int_name(interface_data:list) -> list:

    int_name_lst = list()

    if interface_data != None:
        for interface_name in interface_data.keys():
            int_name_lst.append(interface_name)

    return int_name_lst

    

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks System Informations Converter
#
def _extreme_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key in cmd_outputs.keys():
        if key == INFOS_SYS_DICT_KEY:

            for value in cmd_outputs.get(INFOS_SYS_DICT_KEY):

                sys_info_obj.version = value[0] if value[0] != "" else NOT_SET
                sys_info_obj.hostname = value[1] if value[1] != "" else NOT_SET
                sys_info_obj.model = value[2] if value[2] != "" else NOT_SET
                sys_info_obj.vendor = value[3] if value[3] != "" else NOT_SET
                sys_info_obj.serial = value[4] if value[4] != "" else NOT_SET
                sys_info_obj.base_mac = value[5] if value[5] != "" else NOT_SET


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

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS System Informations Converter
#
def _ios_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key in cmd_outputs.keys():

        if key == INFOS_SYS_DICT_KEY:
            for value in cmd_outputs.get(INFOS_SYS_DICT_KEY):

                sys_info_obj.hostname = value[2] if value[2] != "" else NOT_SET
                sys_info_obj.version = value[0] if value[0] != "" else NOT_SET
                sys_info_obj.model = value[10] if value[10] != "" else NOT_SET
                sys_info_obj.serial = value[7][0] if value[7][0] != "" else NOT_SET
                sys_info_obj.vendor = "Cisco IOS"

        if key == INFOS_SNMP_DICT_KEY:

            for value in cmd_outputs.get(INFOS_SNMP_DICT_KEY):

                sys_info_obj.snmp_ips.append(value[0])

        if key == INFOS_INT_DICT_KEY:

            for value in cmd_outputs.get(INFOS_INT_DICT_KEY):

                sys_info_obj.interfaces_lst.append(
                    _mapping_interface_name(value[0])
                )

    return sys_info_obj

