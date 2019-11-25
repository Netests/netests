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
ERROR_HEADER = "Error import [infos_converters.py]"
HEADER_GET = "[netests - infos_converters]"

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
    print(f"{ERROR_HEADER} protocols.infos")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
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
# NAPALM System Informations Converter
#
def _napalm_infos_converter(plateform:str, cmd_output:dict) -> SystemInfos:

    if cmd_output == None:
        return SystemInfos()

    sys_info_obj = SystemInfos()

    for key in cmd_output.keys():

        # NAPALM get_facts command
        if key ==  INFOS_SYS_DICT_KEY:

            index_fqdn = len(f"{str(cmd_output.get(INFOS_SYS_DICT_KEY).get('facts').get('hostname'))}.")

            # Retrive only physical interfaces
            interface_lst = list()
            if plateform == JUNOS_PLATEFORM_NAME:
                interface_lst = _juniper_retrieve_int_name_with_napalm(
                    cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("interface_list", list)
                )
            elif plateform == CISCO_IOS_PLATEFORM_NAME or plateform == NEXUS_PLATEFORM_NAME:
                interface_lst = _ios_retrieve_int_name_with_napalm(
                    cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("interface_list", list)
                )
            else:
                interface_lst = cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("interface_list", list)


            sys_info_obj.hostname=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("hostname", NOT_SET)
            sys_info_obj.domain=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("fqdn", NOT_SET)[index_fqdn:]
            sys_info_obj.version=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("os_version", NOT_SET)
            sys_info_obj.serial=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("serial_number", NOT_SET)
            sys_info_obj.base_mac=NOT_SET
            sys_info_obj.memory=NOT_SET
            sys_info_obj.vendor=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("vendor", NOT_SET)
            sys_info_obj.model=cmd_output.get(INFOS_SYS_DICT_KEY).get("facts").get("model", NOT_SET)
            sys_info_obj.snmp_ips=list()
            sys_info_obj.interfaces_lst=interface_lst

        # NAPALM get_snmp
        if key == INFOS_SNMP_DICT_KEY:
            pass

    return sys_info_obj

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus System Informations Converter
#
def _cumulus_infos_converter(cmd_outputs:dict) -> SystemInfos:

    if cmd_outputs == None:
        return SystemInfos()

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
# Juniper Network System Informations Converter
#
def _juniper_infos_converter(cmd_outputs:list) -> SystemInfos:

    if cmd_outputs == None:
        return dict()

    sys_info_obj = SystemInfos(
        vendor="Juniper"
    )

    for key, facts in cmd_outputs.items():
        if key == INFOS_SYS_DICT_KEY:

            for element in cmd_outputs.get(INFOS_SYS_DICT_KEY).get("software-information"):

                if "product-model"  in element.keys():
                    sys_info_obj.model = element.get("product-model")[0].get("data", NOT_SET)

                if "junos-version"  in element.keys():
                    sys_info_obj.version = element.get("junos-version")[0].get("data", NOT_SET)


        elif key == INFOS_MEMORY_DICT_KEY:

            sys_info_obj.memory = cmd_outputs.get(INFOS_MEMORY_DICT_KEY).get("system-memory-information")[0].get(
                "system-memory-summary-information")[0].get("system-memory-total")[0].get("data", NOT_SET)

        elif key == INFOS_CONFIG_DICT_KEY:

            sys_info_obj.hostname = cmd_outputs.get(INFOS_CONFIG_DICT_KEY).get("configuration").get("system").get("host-name", NOT_SET)
            sys_info_obj.domain = cmd_outputs.get(INFOS_CONFIG_DICT_KEY).get("configuration").get("system").get("domain-name", NOT_SET)


        elif key == INFOS_SERIAL_DICT_KEY:

            sys_info_obj.serial = \
                cmd_outputs.get(INFOS_SERIAL_DICT_KEY).get("chassis-inventory")[0].get("chassis")[0].get(
                    "serial-number")[0].get("data", NOT_SET)

        elif key == INFOS_INT_DICT_KEY:

            sys_info_obj.interfaces_lst = _juniper_retrieve_int_name(
                cmd_outputs.get(INFOS_INT_DICT_KEY).get("interface-information")[0].get("physical-interface")
            )

    return sys_info_obj

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Network interfacer filter
#
def _juniper_retrieve_int_name(interface_data:dict) -> list:

    int_name_lst = list()

    for interface_name in interface_data:
        if ("em" in interface_name.get("name")[0].get("data", NOT_SET) or \
                "lo" in interface_name.get("name")[0].get("data", NOT_SET)  or \
                "fxp" in interface_name.get("name")[0].get("data", NOT_SET)) and \
                "demux" not in interface_name.get("name")[0].get("data", NOT_SET) and \
                "local" not in interface_name.get("name")[0].get("data", NOT_SET) and \
                interface_name.get("name")[0].get("data", NOT_SET) != NOT_SET:

            int_name_lst.append(
                _mapping_interface_name(interface_name.get("name")[0].get("data"))
            )

    return int_name_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper Network interfacer filter recupered with NAPALM
#
def _juniper_retrieve_int_name_with_napalm(interface_data:list) -> list:

    int_name_lst = list()

    if interface_data != None:
        for interface_name in interface_data:
            if ("em" in interface_name or "lo" in interface_name or "fxp" in interface_name) \
                    and "demux" not in interface_name and "local" not in interface_name:
                int_name_lst.append(
                    _mapping_interface_name(interface_name)
                )

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

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS interfacer filter recupered with NAPALM
#
def _ios_retrieve_int_name_with_napalm(interface_data:list) -> list:
    """
    This function will remove information about Loopback and VLAN interface.
    Goal of the function is to have only physical interfaces

    :param interface_data: List of interfaces retrieve with NAPALM
    :return list: Interfaces list filter with removing virtual interfaces
    """

    int_name_lst = list()

    if interface_data != None:
        for interface_name in interface_data:
            if "LO" not in str(interface_name).upper() and "VL" not in str(interface_name).upper():
                int_name_lst.append(
                    _mapping_interface_name(interface_name)
                )

    return int_name_lst