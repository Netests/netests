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
ERROR_HEADER = "Error import [ipv4.py]"

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
    from protocols.ip import IP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ip")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# IPv4 NEIGHBORS CLASS
#
class IPV4(IP):

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, interface_name=NOT_SET, ip_address_with_mask=NOT_SET, netmask=NOT_SET):

        if netmask == NOT_SET:
            ip_address = self._extract_ip_address(ip_address_with_mask)
            netmask = self._extract_netmask(ip_address_with_mask)
        else:
            ip_address = ip_address_with_mask

        if self._is_valid_cidr_netmask(netmask):
            netmask = self._convert_cidr_to_netmask(netmask)

        if self._is_valid_ip_and_mask(ip_address, netmask):
            super().__init__(interface_name, ip_address, netmask)
        else:
            super().__init__(NOT_SET, NOT_SET, NOT_SET)
    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_ip_and_mask(self, ip_address, netmask) -> bool:
        """
        This function will check if an IP address and the netmask given in parameter are correct.

        :param ip_address: IPv4 address to check
        :param netmask: Netmask in CIDR (/24) or 255.255.255.255 format
        :return: False if one or more of the two values is false
        """

        return_value = self._is_valid_ipv4_address(ip_address)

        if self._is_cidr_notation(netmask):
            return return_value and self._is_valid_cidr_netmask(netmask)
        else:
            return return_value and self._is_valid_netmask(netmask)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_cidr_notation(self, netmask) -> bool:
        """
        This function will check if the netmask is in CIDR format.

        :param netmask: Can be a 255.255.255.255 or CIDR /24 format
        :return bool: True if mask is in CIDR format
        """

        return "." not in str(netmask)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _convert_cidr_to_netmask(self, netmask_cidr:str) -> str:
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
    def _convert_netmask_to_cidr(self, netmask:str) -> str:
        """
        This function will convert a netmask in a CIDR format.

        :param netmask: IP address netmask in 255.255.255.255 format
        :return str: IP address mask in CIDR format (/24)
        """

        if (self._is_valid_netmask(netmask)):
            netmask_in_bits = self._convert_in_bit_format(netmask)
            index_first_zero = netmask_in_bits.find("0")
            return  index_first_zero

        return None
    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_ipv4_address(self, ip_address) -> bool:
        """
        This function will check is the ip_address given is parameter is a valid IP address.

        :param ip_address: IP address to check
        :return bool: True if ip_address is a valid IP address
        """

        return ipaddress.IPv4Address(ip_address)


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_cidr_netmask(self, cidr_netmask:str) -> bool:
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
    def _is_valid_netmask(self, netmask:str) -> bool:
        """
        This function will check that the netmask given in parameter is a correct mask for IPv4 IP address.
        Using to verify a netmask in 255.255.255.255 format.

        :param netmask: Netmask to check
        :return bool: True if the netmask is valid
        """

        netmask_in_bits = self._convert_in_bit_format(netmask)

        assert netmask_in_bits.__len__() == 32

        index_first_zero = netmask_in_bits.find("0")

        if netmask_in_bits.find("0") != -1:
            if netmask_in_bits[index_first_zero:].find("1") != -1:
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _extract_ip_address(self, ip_address_with_netmask, separator="/") -> str:
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
    def _extract_netmask(self, ip_address_with_netmask, separator="/") -> str:
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
    def _convert_in_bit_format(self, ip_value) -> str:
        """
        This function will receive a value in parameter an convert it in a bit format.

        :param ip_value: Can be a mask or an IP address
        :return str: ip_value in bit format
        """

        all_bytes = ip_value.split  (".")

        assert all_bytes.__len__() == 4

        bit_format = ""
        for bytes in all_bytes:
            # [2:] for remove "0b"
            bit_format = bit_format + str(bin(int(bytes))[2:].zfill(8))

        return bit_format


########################################################################################################################
#
# IPv4 LIST CLASS
#
class ListIPV4:

    hostname: str
    ipv4_addresses_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname:NOT_SET, ipv4_addresses_lst: list()):
        self.hostname = hostname
        self.ipv4_addresses_lst = ipv4_addresses_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListIPV4):
            raise NotImplemented

        for ipv4 in self.ipv4_addresses_lst:
            if ipv4 not in others.ipv4_addresses_lst:
                print(
                    f"[ListIPV4 - __eq__] - The following IPv4 address is not in the list \n {ipv4}")
                print(
                    f"[ListIPV4 - __eq__] - List: \n {others.ipv4_addresses_lst}")
                return False

        for ipv4 in others.ipv4_addresses_lst:
            if ipv4 not in self.ipv4_addresses_lst:
                print(
                    f"[ListIPV4 - __eq__] - The following IPv4 address is not in the list \n {ipv4}")
                print(
                    f"[ListIPV4 - __eq__] - List: \n {self.ipv4_addresses_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = f"<ListIPV4 hostname={self.hostname} \n"
        for ipv4 in self.ipv4_addresses_lst:
            result = result + f"{ipv4}"
        return result + ">"