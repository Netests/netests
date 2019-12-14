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
ERROR_HEADER = "Error import [ipv6.py]"

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
# IPV6 NEIGHBORS CLASS
#
class IPV6(IP):

    ip_address: str
    interface_name: str

    def __init__(self, interface_name=NOT_SET, ip_address_with_mask=NOT_SET,):

        index_slash = str(ip_address_with_mask).find("/")

        super().__init__(
            interface_name=interface_name,
            ip_address=ip_address_with_mask[:index_slash],
            netmask=ip_address_with_mask[index_slash+1:]
        )

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_ip_and_mask(self, ip_address, netmask) -> bool:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_ipv6_address(self, ip_address) -> bool:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _is_valid_netmask(self, netmask):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _extract_ip_address(self, ip_address_with_netmask, separator="/") -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def _extract_netmask(self, ip_address_with_netmask, separator="/") -> str:
        pass


########################################################################################################################
#
# IPV6 LIST CLASS
#
class ListIPV6:

    hostname: str
    ipv6_addresses_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname:NOT_SET, ipv6_addresses_lst: list()):
        self.hostname = hostname
        self.ipv6_addresses_lst = ipv6_addresses_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListIPV6):
            raise NotImplemented

        for ipv6 in self.ipv6_addresses_lst:
            if ipv6 not in others.ipv6_addresses_lst:
                print(
                    f"[ListIPV6 - __eq__] - The following IPv6 address is not in the list \n {ipv6}")
                print(
                    f"[ListIPV6 - __eq__] - List: \n {others.ipv6_addresses_lst}")
                return False

        for ipv6 in others.ipv6_addresses_lst:
            if ipv6 not in self.ipv6_addresses_lst:
                print(
                    f"[ListIPV6 - __eq__] - The following IPv6 address is not in the list \n {ipv6}")
                print(
                    f"[ListIPV6 - __eq__] - List: \n {self.ipv6_addresses_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = f"<ListIPV6 hostname={self.hostname} \n"
        for ipv6 in self.ipv6_addresses_lst:
            result = result + f"{ipv6}"
        return result + ">"