#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.facts import Facts
from netests.mappings import mapping_interface_name
from netests.constants import (
    NOT_SET,
    CISCO_IOS_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME
)


def _napalm_facts_converter(
    hostname: str,
    cmd_output: json,
    options={}
) -> Facts:
    if cmd_output is None:
        return Facts()

    i = len(f"{str(cmd_output.get('facts').get('hostname'))}.")

    facts = Facts(
        hostname=cmd_output.get('facts').get('hostname')
                    if cmd_output.get("facts").get("hostname", NOT_SET)
                        != '' else NOT_SET,
        domain=cmd_output.get("facts").get("fqdn", NOT_SET)[i:]
                    if cmd_output.get("facts").get("fqdn", NOT_SET)
                        != '' else NOT_SET,
        version=cmd_output.get("facts").get("os_version", NOT_SET)
                    if cmd_output.get("facts").get("os_version", NOT_SET)
                        != '' else NOT_SET,
        serial=cmd_output.get("facts").get("serial_number", NOT_SET)
                    if cmd_output.get("facts").get("serial_number", NOT_SET)
                        != '' else NOT_SET,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor=cmd_output.get("facts").get("vendor", NOT_SET)
                    if cmd_output.get("facts").get("vendor", NOT_SET)
                        != '' else NOT_SET,
        model=cmd_output.get("facts").get("model", NOT_SET)
                    if cmd_output.get("facts").get("model", NOT_SET)
                        != '' else NOT_SET,
        interfaces_lst=cmd_output.get('facts').get('interface_list')
                    if cmd_output.get("facts").get("interface_list", NOT_SET)
                        != '' else [],
        options=options
    )

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
    if interface_data is not None:
        for interface_name in interface_data:
            if (
                (
                    "em" in interface_name or
                    "lo" in interface_name or
                    "fxp" in interface_name
                ) and
                "demux" not in interface_name and
                "local" not in interface_name
            ):
                int_name_lst.append(
                    mapping_interface_name(interface_name)
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

    if interface_data is not None:
        for interface_name in interface_data:
            if (
                "LO" not in str(interface_name).upper() and
                "VL" not in str(interface_name).upper()
            ):
                int_name_lst.append(
                    mapping_interface_name(interface_name)
                )

    return int_name_lst
