#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import (
    NOT_SET,
    BGP_STATE_UP_LIST,
    BGP_STATE_BRIEF_UP,
    BGP_STATE_BRIEF_DOWN,
    BGP_UPTIME_FORMAT_MS
)


def get_bgp_state_brief(state: str) -> str:
    if state in BGP_STATE_UP_LIST:
        return BGP_STATE_BRIEF_UP
    else:
        return BGP_STATE_BRIEF_DOWN


def get_bgp_peer_uptime(value: str, format: str) -> str:
    if format == BGP_UPTIME_FORMAT_MS:
        return value


def mapping_sys_capabilities(code) -> str():
    """
    This function will return systeme capability name
    regarding the abreviation given in parameter

    Output extract from Cisco Nexus 9000v Chassis NXOS: version 7.0(3)I7(5a)

    Capability codes:
    (R) Router, (B) Bridge, (T) Telephone, (C) DOCSIS Cable Device
    (W) WLAN Access Point, (P) Repeater, (S) Station, (O) Other

    :param codes: str()
    :return str(): that contains system capability name
    """

    if code == "R" or code.upper() == "ROUTER":
        return "Router"
    elif code == "B":
        return "Bridge"
    elif code == "T":
        return "Telephone"
    elif code == "C":
        return "DOCSIS Cable Device"
    elif code == "W":
        return "WLAN Access Point"
    elif code == "P":
        return "Repeater"
    elif code == "S":
        return "Station"
    elif code == "O":
        return "Other"
    else:
        return NOT_SET


def get_first_digit_index(string: str) -> int:
    """
    This function will return the index of the first index of a string.
    return -1 if no digit

    :param string: String on which one find a digit
    :return: Index of the first digit
    """
    index = 0
    find = False

    for char in str(string):
        if not find:
            if char.isdigit():
                find = True
            else:
                index = index + 1

    if not find:
        return -1
    return index


def mapping_interface_name(int_name) -> str():
    """
    This function will receive an interface name in parameter
    and return the standard interface name.

    For example:
        * (Arista) Ethernet3 => Eth1/3

    :param int_name:
    :return:
    """

    if (
        "Ethernet1/" in int_name and
        "GIGABITETHERNET" not in str(int_name).upper()
    ):
        number = ""
        slash_index = int_name.find("/")
        for char in int_name[slash_index:]:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    elif (
        "Ethernet" in int_name and
        "GIGABITETHERNET" not in str(int_name).upper()
    ):
        number = ""
        for char in int_name:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    elif "LOOPBACK" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("lo").lower() + int_name[index:]

    elif "MANAGEMENT" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("mgmt").lower() + int_name[index:]

    elif "GIGABITETHERNET" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("Gi") + str(int_name)[index:]

    elif "Gi" in str(int_name):
        index = get_first_digit_index(int_name)
        return str("Gi") + str(int_name)[index:]

    # Extreme VSP - Loopback converter
    # (Clip1        10.255.255.102 255.255.255.255)
    elif "Clip" in str(int_name):
        index = get_first_digit_index(int_name)
        return str("lo") + str(int_name)[index:]

    elif str(int_name) == NOT_SET:
        return int_name

    else:
        return str(int_name).lower()
