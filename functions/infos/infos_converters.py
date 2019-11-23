#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [bgp_converters.py]"
HEADER_GET = "[netests - bgp_converters]"

########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.infos import SystemInfos
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM infos converter
#
def _napalm_infos_converter(status:str) -> str:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus BGP converter
#
def _cumulus_infos_converter(cmd_outputs:dict) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key, facts in cmd_outputs.items():

        if key == INFOS_SYS_DICT_KEY:
            sys_info_obj.hostname = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("hostname", NOT_SET)
            sys_info_obj.version = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("os-version", NOT_SET)
            sys_info_obj.serial = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("eeprom").get("tlv").get("Serial Number").get("value", NOT_SET)
            sys_info_obj.base_mac = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("eeprom").get("tlv").get("Base MAC Address").get("value", NOT_SET)
            sys_info_obj.memory = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("memory", NOT_SET)
            sys_info_obj.vendor = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("eeprom").get("tlv").get("Vendor Name", NOT_SET).get("value", NOT_SET)
            sys_info_obj.model = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("platform", NOT_SET).get("model", NOT_SET)

        elif key == INFOS_SNMP_DICT_KEY:

            sys_info_obj.snmp_ips = cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("ListeningIPAddresses", NOT_SET)

        elif key == INFOS_INT_DICT_KEY:

            sys_info_obj.interfaces_lst = _cumulus_retrieve_int_name(cmd_outputs.get(INFOS_INT_DICT_KEY))

    return sys_info_obj

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus interface filter
#
def _cumulus_retrieve_int_name(interface_data:dict) -> list:

    int_name_lst = list()

    if interface_data != None:
        for intferce_name in interface_data.keys():
            if "swp" in intferce_name or "eth" in intferce_name:
                int_name_lst.append(intferce_name)

    return int_name_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus BGP Converter
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
            sys_info_obj.snmp_ips = cmd_outputs.get(INFOS_SNMP_DICT_KEY).get("TABLE_host", NOT_SET).get("ROW_host").get("host")

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
# Arista BGP Converter
#
def _arista_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos()

    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:

            sys_info_obj.version = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("version", NOT_SET)
            sys_info_obj.serial = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("serialNumber", NOT_SET)
            sys_info_obj.base_mac = NOT_SET
            sys_info_obj.memory = cmd_outputs.get(INFOS_SYS_DICT_KEY).get("memFree", NOT_SET)
            sys_info_obj.vendor = "Arista Networks"
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
        for intferce_name in interface_data.keys():
            int_name_lst.append(intferce_name)

    return int_name_lst