#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import json
import ipaddress
from netests import log
from nornir.core import Nornir
from netmiko import ConnectHandler
from netests.constants import (
    NOT_SET,
    NETMIKO_NAPALM_MAPPING_PLATEFORM,
    BGP_STATE_UP_LIST,
    BGP_STATE_BRIEF_UP,
    BGP_STATE_BRIEF_DOWN
)


ERROR_HEADER = "Error import [global.py]"


def _generic_state_converter(state: str) -> str:
    """
    This function will convert session state in a session state brief.
    The result can be UP or DOWN.
    Example : Idle => Down

    :param state:
    :return str: State brief
    """

    if state in BGP_STATE_UP_LIST or state == NOT_SET:
        return BGP_STATE_BRIEF_UP
    else:
        return BGP_STATE_BRIEF_DOWN


def check_devices_connectivity(nr: Nornir) -> bool:
    """
    This function will test the connectivity to each devices

    :param nr:
    :return bool: True if ALL devices are reachable
    """

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{ERROR_HEADER}] no device selected.")

    data = devices.run(task=is_alive, num_workers=100)
    # print_result(data)

    for device in devices.inventory.hosts:
        if data[device].failed:
            print(f"\t--> Connection to {device} has failed.")

    if not data.failed:
        print("All devices are reachable :) !")
    else:
        print("\nPlease check credentials in the inventory")

    return not data.failed


def is_alive(task) -> None:
    """
    This function will use Netmiko find_prompt() function to test connectivity
    :param task:
    :return None:
    """

    if task.host.platform in NETMIKO_NAPALM_MAPPING_PLATEFORM.keys():
        platform = NETMIKO_NAPALM_MAPPING_PLATEFORM.get(task.host.platform)
    else:
        platform = task.host.platform

    try:
        print(platform)
        device = ConnectHandler(
            device_type=platform,
            host=task.host.hostname,
            username=task.host.username,
            password=task.host.password,
        )
        log.debug(device)
    except Exception:
        return False

    return True


def _generic_interface_filter(
    plateform,
    iname,
    *,
    filters=dict()
) -> bool:

    if (
        "linux" in plateform and "bridge" not in iname and
            (
                (
                    filters.get('get_vlan', True) and
                    "vlan" in iname
                ) or
                (
                    filters.get('get_loopback', True) and
                    "lo" in iname
                ) or
                (
                    filters.get('get_peerlink', True) and
                    "peerlink" in iname
                ) or
                (
                    filters.get('get_vni', True) and
                    "vni" in iname
                ) or
                (
                    filters.get('get_physical', True) and
                    ("swp" in iname or "eth" in iname)
                )
            )
    ):
        return True

    elif (
        "nxos" in plateform and
        (
            (
                filters.get('get_vlan', True) and
                "VLAN" in str(iname).upper()
            ) or
            (
                filters.get('get_loopback', True) and
                "LO" in str(iname).upper()
            ) or
            (
                filters.get('get_physical', True) and
                (
                    "ETH" in str(iname).upper() or
                    "MGMT" in str(iname).upper()
                )
            )
        )
    ):
        return True

    elif (
        "eos" in plateform and
        (
            (
                filters.get('get_vlan', True) and
                "VLAN" in str(iname).upper()
            ) or
            (
                filters.get('get_loopback', True) and
                "LO" in str(iname).upper()
            ) or
            (
                filters.get('get_physical', True) and
                (
                    "ETH" in str(iname).upper() or
                    "MGMT" in str(iname).upper()
                )
            )
        )
    ):
        return True

    elif (
        "ios" in plateform and
        (
            (
                filters.get('get_vlan', True) and
                "." in str(iname).upper()
            ) or
            (
                filters.get('get_loopback', True)
                and "LO" in str(iname).upper()
            ) or
            (
                filters.get('get_physical', True) and
                (
                    "GI" in str(iname).upper() or
                    "MGMT" in str(iname).upper()
                )
            )
        )
    ):
        return True

    elif (
        "junos" in plateform and
        (
            (
                filters.get('get_vlan', True) and
                "VLAN" in str(iname).upper()
            ) or
            (
                filters.get('get_loopback', True) and
                "LO" in str(iname).upper()
            ) or
            (
                filters.get('get_physical', True) and
                (
                    "EM" in str(iname).upper() or
                    "FXP" in str(iname).upper() or
                    "GE" in str(iname).upper()
                )
            )
        )
    ):
        return True

    elif (
        "extreme_vsp" in plateform and
        (
            (
                filters.get('get_vlan', True) and
                "VLAN" in str(iname).upper()
            ) or
            (
                filters.get('get_loopback', True) and
                "LO" in str(iname).upper()
            ) or
            (
                filters.get('get_physical', True) and
                (
                    "PORT" in str(iname).upper() or
                    "MGMT" in str(iname).upper()
                )
            )
        )
    ):
        return True

    return False


def is_valid_ip_and_mask(ip_address, netmask) -> bool:
    """
    This function will check if an IP address and
    the netmask given in parameter are correct.

    :param ip_address: IPv4 address to check
    :param netmask: Netmask in CIDR (/24) or 255.255.255.255 format
    :return: False if one or more of the two values is false
    """

    return_value = is_valid_ipv4_address(ip_address)

    if is_cidr_notation(netmask):
        return return_value and is_valid_cidr_netmask(netmask)
    else:
        return return_value and is_valid_netmask(netmask)


def is_cidr_notation(netmask) -> bool:
    """
    This function will check if the netmask is in CIDR format.

    :param netmask: Can be a 255.255.255.255 or CIDR /24 format
    :return bool: True if mask is in CIDR format
    """

    return "." not in str(netmask)


def convert_cidr_to_netmask(netmask_cidr: str) -> str:
    """
    This function will convert a netmask CIDR in a standard netmask (255.0.0.0)
    :param netmask_cidr: IP address netmask in CIDR format (/24)
    :return str: IP address netmask in 255.255.255.255 format
    """
    bits = 0

    for i in range(32 - int(netmask_cidr), 32):
        bits |= (1 << i)
    return (
        "%d.%d.%d.%d" %
        (
            (bits & 0xff000000) >> 24,
            (bits & 0xff0000) >> 16,
            (bits & 0xff00) >> 8,
            (bits & 0xff)
        )
    )


def convert_netmask_to_cidr(netmask: str) -> str:
    """
    This function will convert a netmask in a CIDR format.

    :param netmask: IP address netmask in 255.255.255.255 format
    :return str: IP address mask in CIDR format (/24)
    """

    if (is_valid_netmask(netmask)):
        netmask_in_bits = convert_in_bit_format(netmask)
        index_first_zero = netmask_in_bits.find("0")
        return index_first_zero

    return None


def is_valid_ipv4_address(ip_address) -> bool:
    """
    This function will check is the ip_address given is
    parameter is a valid IP address.

    :param ip_address: IP address to check
    :return bool: True if ip_address is a valid IP address
    """

    try:
        ipaddress.IPv4Address(ip_address)
        return True
    except ipaddress.AddressValueError:
        return False


def is_valid_cidr_netmask(cidr_netmask: str) -> bool:
    """
    This function will check that the netmask given in
    parameter is a correct mask for IPv4 IP address.
    Using to verify a netmask in CIDR (/24) format.

    :param cidr_netmask: Netmask to check
    :return bool: True if the netmask is valid
    """

    return str(cidr_netmask).isdigit() and \
        int(cidr_netmask) >= 0 and \
        int(cidr_netmask) <= 32


def is_valid_netmask(netmask: str) -> bool:
    """
    This function will check that the netmask given
    in parameter is a correct mask for IPv4 IP address.
    Using to verify a netmask in 255.255.255.255 format.

    :param netmask: Netmask to check
    :return bool: True if the netmask is valid
    """

    netmask_in_bits = convert_in_bit_format(netmask)

    assert netmask_in_bits.__len__() == 32

    index_first_zero = netmask_in_bits.find("0")

    if netmask_in_bits.find("0") != -1:
        if netmask_in_bits[index_first_zero:].find("1") != -1:
            return False

    return True


def extract_ip_address(ip_address_with_netmask, separator="/") -> str:
    """
    This function will extract netmask from an
    'IP address with netmask' receive in parameter.
    Separator is the char that separate ip_address of netmask. Example :

        a) 192.168.1.1/24               - separator='/'
        b) 192.168.1.1 24               - separtor =' '
        c) 192.168.1.1 255.255.255.0    - separtor =' '

    Separtor value can not be '.' or a digit...

    :param ip_address_with_netmask: IP address with the netmask
            (192.168.1.1/24 or 192.168.1.1 255.255.255.0)
    :param separator: Char that separate ip_address of netmask
    :return: ip_address value
    """

    if separator.isdigit() is False and separator != ".":
        index = (ip_address_with_netmask.find(separator))
        return ip_address_with_netmask[:index]
    else:
        raise Exception


def extract_netmask(ip_address_with_netmask, separator="/") -> str:
    """
    This function will extract netmask from an
    'IP address with netmask' receive in parameter.
    Separator is the char that separate ip_address of netmask. Example :

        a) 192.168.1.1/24               - separator='/'
        b) 192.168.1.1 24               - separtor =' '
        c) 192.168.1.1 255.255.255.0    - separtor =' '

    Separtor value can not be '.' or a digit...

    :param ip_address_with_netmask: IP address with the netmask (1.1.1.1/24)
    :param separator: Char that separate ip_address of netmask
    :return: Netmask value can be (255.255.255.0 or 24)
    """
    if separator.isdigit() is False and separator != ".":
        index = (ip_address_with_netmask.find(separator) + 1)
        return ip_address_with_netmask[index:]
    else:
        raise Exception


def convert_in_bit_format(ip_value) -> str:
    """
    This function will receive a value in parameter an
    convert it in a bit format.

    :param ip_value: Can be a mask or an IP address
    :return str: ip_value in bit format
    """

    all_bytes = ip_value.split(".")

    assert all_bytes.__len__() == 4

    bit_format = ""
    for bytes in all_bytes:
        # [2:] for remove "0b"
        bit_format = bit_format + str(bin(int(bytes))[2:].zfill(8))

    return bit_format


def open_file(path: str()) -> dict():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the yaml file

    Returns:
        dict: file content
    """

    with open(path, 'r') as yamlFile:
        try:
            data = yaml.load(yamlFile, Loader=yaml.FullLoader)
        except yaml.YAMLError as exc:
            print(exc)

    return data


def open_txt_file_as_bytes(path: str()) -> str():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the string file

    Returns:
        str: file content
    """

    with open(path, 'rb') as content_file:
        try:
            content = content_file.read()
        except Exception as exc:
            print(exc)

    return content


def open_txt_file(path: str()) -> str():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the string file

    Returns:
        str: file content
    """

    with open(path, 'r') as content_file:
        try:
            content = content_file.read()
        except Exception as exc:
            print(exc)

    return content


def open_json_file(path: str()) -> str():
    """
        This function  will open a json file and return is data

        Args:
            param1 (str): Path to the string file

        Returns:
            str: file content
        """

    with open(path, 'r') as content_file:
        try:
            content = json.loads(content_file.read())
        except yaml.YAMLError as exc:
            print(exc)

    return content
