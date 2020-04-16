#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.facts import Facts
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from functions.discovery_protocols.discovery_functions import (
    _mapping_interface_name
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_DATA_HOST_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_SNMP_DICT_KEY,
    CISCO_IOS_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _napalm_facts_converter(
    hostname: str,
    platform: str,
    cmd_output: json,
    options={}
) -> Facts:
    if cmd_output == None:
        return Facts()

    i = len(f"{str(cmd_output.get('facts').get('hostname'))}.")

    facts = Facts(   
        hostname=cmd_output.get('facts').get('hostname'),
        domain=cmd_output.get("facts").get("fqdn", NOT_SET)[i:],
        version=cmd_output.get("facts").get("os_version", NOT_SET),
        serial=cmd_output.get("facts").get("serial_number", NOT_SET),
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor=cmd_output.get("facts").get("vendor", NOT_SET),
        model=cmd_output.get("facts").get("model", NOT_SET),
        interfaces_lst=cmd_output.get('facts').get('interface_list'),
        options=options
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        PP.pprint(facts.to_json())

    return facts


def _interfaces_filter(platform: str, interfaces: list) -> list:
    if platform == JUNOS_PLATEFORM_NAME:
        return _juniper_retrieve_int_name_with_napalm(interfaces)
    elif (
        platform == CISCO_IOS_PLATEFORM_NAME or
        platform == NEXUS_PLATEFORM_NAME
    ):
        return _ios_retrieve_int_name_with_napalm(interfaces)
    else:
        return interfaces


def _juniper_retrieve_int_name_with_napalm(interface_data: list) -> list:

    int_name_lst = list()

    if interface_data != None:
        for interface_name in interface_data:
            if (
                ("em" in interface_name or 
                "lo" in interface_name or
                "fxp" in interface_name) and
                "demux" not in interface_name and
                "local" not in interface_name
            ):
                int_name_lst.append(
                    _mapping_interface_name(interface_name)
                )

    return int_name_lst



def _ios_retrieve_int_name_with_napalm(interface_data: list) -> list:
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
