#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [global.py]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import ipaddress
except ImportError as importError:
    print(f"{ERROR_HEADER} ipaddress")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    print(importError)
    exit(EXIT_FAILURE)

# ------------------------------------------------------------------------------------------------------------------
#
#
def is_valid_ip_and_mask(ip_address, netmask) -> bool:
    """
    This function will check if an IP address and the netmask given in parameter are correct.

    :param ip_address: IPv4 address to check
    :param netmask: Netmask in CIDR (/24) or 255.255.255.255 format
    :return: False if one or more of the two values is false
    """

    return_value = is_valid_ipv4_address(ip_address)

    if is_cidr_notation(netmask):
        return return_value and is_valid_cidr_netmask(netmask)
    else:
        return return_value and is_valid_netmask(netmask)


# ------------------------------------------------------------------------------------------------------------------
#
#
def is_cidr_notation(netmask) -> bool:
    """
    This function will check if the netmask is in CIDR format.

    :param netmask: Can be a 255.255.255.255 or CIDR /24 format
    :return bool: True if mask is in CIDR format
    """

    return "." not in str(netmask)


# ------------------------------------------------------------------------------------------------------------------
#
#
def convert_cidr_to_netmask(netmask_cidr: str) -> str:
    """
    This function will convert a netmask CIDR in a standard netmask (255.255.255.255)
    :param netmask_cidr: IP address netmask in CIDR format (/24)
    :return str: IP address netmask in 255.255.255.255 format
    """
    bits = 0

    for i in range(32 - int(netmask_cidr), 32):
        bits |= (1 << i)
    return "%d.%d.%d.%d" % ((bits & 0xff000000) >> 24, (bits & 0xff0000) >> 16, (bits & 0xff00) >> 8, (bits & 0xff))


# ------------------------------------------------------------------------------------------------------------------
#
#
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


# ------------------------------------------------------------------------------------------------------------------
#
#
def is_valid_ipv4_address(ip_address) -> bool:
    """
    This function will check is the ip_address given is parameter is a valid IP address.

    :param ip_address: IP address to check
    :return bool: True if ip_address is a valid IP address
    """

    return ipaddress.IPv4Address(ip_address)


# ------------------------------------------------------------------------------------------------------------------
#
#
def is_valid_cidr_netmask(cidr_netmask: str) -> bool:
    """
    This function will check that the netmask given in parameter is a correct mask for IPv4 IP address.
    Using to verify a netmask in CIDR (/24) format.

    :param cidr_netmask: Netmask to check
    :return bool: True if the netmask is valid
    """

    return str(cidr_netmask).isdigit() and \
           int(cidr_netmask) >= 0 and \
           int(cidr_netmask) <= 32


# ------------------------------------------------------------------------------------------------------------------
#
#
def is_valid_netmask(netmask: str) -> bool:
    """
    This function will check that the netmask given in parameter is a correct mask for IPv4 IP address.
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


# ------------------------------------------------------------------------------------------------------------------
#
#
def extract_ip_address(ip_address_with_netmask, separator="/") -> str:
    """
    This function will extract netmask from an 'IP address with netmask' receive in parameter.
    Separator is the char that separate ip_address of netmask. Example :

        a) 192.168.1.1/24               - separator='/'
        b) 192.168.1.1 24               - separtor =' '
        c) 192.168.1.1 255.255.255.0    - separtor =' '

    Separtor value can not be '.' or a digit...

    :param ip_address_with_netmask: IP address with the netmask (192.168.1.1/24 or 192.168.1.1 255.255.255.0)
    :param separator: Char that separate ip_address of netmask
    :return: ip_address value
    """

    if separator.isdigit() is False and separator != ".":
        index = (ip_address_with_netmask.find(separator))
        return ip_address_with_netmask[:index]
    else:
        raise Exception


# ------------------------------------------------------------------------------------------------------------------
#
#
def extract_netmask(ip_address_with_netmask, separator="/") -> str:
    """
    This function will extract netmask from an 'IP address with netmask' receive in parameter.
    Separator is the char that separate ip_address of netmask. Example :

        a) 192.168.1.1/24               - separator='/'
        b) 192.168.1.1 24               - separtor =' '
        c) 192.168.1.1 255.255.255.0    - separtor =' '

    Separtor value can not be '.' or a digit...

    :param ip_address_with_netmask: IP address with the netmask (192.168.1.1/24)
    :param separator: Char that separate ip_address of netmask
    :return: Netmask value can be (255.255.255.0 or 24)
    """
    if separator.isdigit() is False and separator != ".":
        index = (ip_address_with_netmask.find(separator) + 1)
        return ip_address_with_netmask[index:]
    else:
        raise Exception


# ------------------------------------------------------------------------------------------------------------------
#
#
def convert_in_bit_format(ip_value) -> str:
    """
    This function will receive a value in parameter an convert it in a bit format.

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

# ----------------------------------------------------------------------------------------------------------------------
#
# Open a YAML File and open VM_path contains into YAML file
#
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
            data = yaml.load(yamlFile)
        except yaml.YAMLError as exc:
            print(exc)

    return data

# ----------------------------------------------------------------------------------------------------------------------
#
# Open a YAML File and open VM_path contains into YAML file
#
def open_txt_file(path: str()) -> str():
    """
    This function  will open a yaml file and return is data

    Args:
        param1 (str): Path to the string file

    Returns:
        str: file content
    """

    with open(path, 'r') as content_file   :
        try:
            content = content_file.read()
        except yaml.YAMLError as exc:
            print(exc)

    return content

