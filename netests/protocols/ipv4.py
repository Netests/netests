#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from netests.constants import NOT_SET
from netests.protocols.ip import IPAddress


class IPV4(IPAddress):

    @classmethod
    def deserialize(
        cls,
        ip_address=NOT_SET,
        netmask=NOT_SET
    ) -> "IPV4":
        if IPV4._is_valid_ipv4_and_mask(ip_address, netmask):
            return {
                "ip_address": ip_address,
                "netmask": netmask
            }
        else:
            return {
                "ip_address": NOT_SET,
                "netmask": NOT_SET
            }

    def _is_valid_ipv4_and_mask(self, ip_address, netmask) -> bool:
        """
        This function will check if an IP address and the netmask are correct.

        :param ip_address: IPv4 address to check
        :param netmask: Netmask in CIDR (/24) or 255.255.255.255 format
        :return: False if one or more of the two values is false
        """

        return_value = self._is_valid_ipv4_address(ip_address)

        if self._is_cidr_notation(netmask):
            return return_value and self._is_valid_cidr_netmask(netmask)
        else:
            return return_value and self._is_valid_netmask(netmask)

    def _is_valid_ipv4_address(self, ip_address) -> bool:
        """
        This function will check is the ip_address is a valid IP address.

        :param ip_address: IP address to check
        :return bool: True if ip_address is a valid IP address
        """

        try:
            ipaddress.IPv4Address(ip_address)
            return True
        except ipaddress.AddressValueError:
            return False

    def _is_cidr_notation(self, netmask) -> bool:
        """
        This function will check if the netmask is in CIDR format.

        :param netmask: Can be a 255.255.255.255 or CIDR /24 format
        :return bool: True if mask is in CIDR format
        """

        return "." not in str(netmask)

    def _is_valid_cidr_netmask(self, cidr_netmask: str) -> bool:
        """
        This function will check if the netmask is a correct mask.
        Using to verify a netmask in CIDR (/24) format.

        :param cidr_netmask: Netmask to check
        :return bool: True if the netmask is valid
        """

        return str(cidr_netmask).isdigit() and \
            int(cidr_netmask) >= 0 and \
            int(cidr_netmask) <= 32

    def _is_valid_netmask(self, netmask: str) -> bool:
        """
        This function will check if the netmask is a correct mask.
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

    def _convert_in_bit_format(self, ip_value) -> str:
        """
        This function will receive a value an convert it in a bit format.

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
