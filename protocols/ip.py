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
ERROR_HEADER = "Error import [ip.py]"

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
    from functions.global_tools import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from abc import ABC, abstractmethod
except ImportError as importError:
    print(f"{ERROR_HEADER} abc")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# IP Address
#
class IPAddress():

    ip_address: str
    netmask: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ip_address="0.0.0.0", netmask="0.0.0.0"):
        self.ip_address = ip_address

        if is_cidr_notation(netmask):
            self.netmask = convert_cidr_to_netmask(netmask)
        else:
            self.netmask = netmask

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, IP):
            return NotImplemented

        return (str(self.ip_address) == str(other.ip_address) and
                str(self.netmask) == str(other.netmask))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<{type(self)} ip_address={self.ip_address} " \
               f"netmask={self.netmask}>\n"

########################################################################################################################
#
# IPAddress LIST CLASS
#
class ListIPAddress:

    ip_addresses_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ip_addresses_lst: list()):
        self.ip_addresses_lst = ip_addresses_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListIPAddress):
            raise NotImplemented

        for ip_address in self.ip_addresses_lst:
            if ip_address not in others.ip_addresses_lst:
                print(
                    f"[ListIPAddress - __eq__] - The following IPAddress is not in the list \n {ip_address}")
                print(
                    f"[ListIPAddress - __eq__] - List: \n {others.ip_addresses_lst}")
                return False

        for ip_address in others.ip_addresses_lst:
            if ip_address not in self.ip_addresses_lst:
                print(
                    f"[ListIPAddress - __eq__] - The following IPAddress is not in the list \n {ip_address}")
                print(
                    f"[ListIPAddress - __eq__] - List: \n {self.ip_addresses_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListIPAddress \n"
        for ip_address in self.ip_addresses_lst:
            result = result + f"{ip_address}"
        return result + ">"



########################################################################################################################
#
# IP Abstract Class
#
class IP(ABC):

    interface_name: str
    ip_address: str
    netmask: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, interface_name=NOT_SET, ip_address=NOT_SET, netmask=NOT_SET):
        self.interface_name = interface_name
        self.ip_address = ip_address
        self.netmask = netmask

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, IP):
            return NotImplemented

        return (str(self.interface_name) == str(other.interface_name) and
                str(self.ip_address) == str(other.ip_address) and
                str(self.netmask) == str(other.netmask))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<{type(self)} interface_name={self.interface_name} " \
               f"ip_address={self.ip_address} " \
               f"netmask={self.netmask}>\n"

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    @abstractmethod
    def _is_valid_ip_and_mask(self, ip_address, netmask) -> bool:
        pass


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    @abstractmethod
    def _is_valid_netmask(self, netmask):
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    @abstractmethod
    def _extract_ip_address(self, ip_address_with_netmask, separator="/") -> str:
        pass

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    @abstractmethod
    def _extract_netmask(self, ip_address_with_netmask, separator="/") -> str:
        pass