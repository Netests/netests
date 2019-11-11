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
    from abc import ABC, abstractmethod
except ImportError as importError:
    print(f"{ERROR_HEADER} abc")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Discovery Protocols Abstract CLASS
#
class IP(ABC):

    ip_address: str
    netmask: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ip_address=NOT_SET, netmask=NOT_SET):
        self.ip_address = ip_address
        self.netmask = netmask

    @abstractmethod
    def __init__(self, netmask_with_cidr=NOT_SET, ):
        pass

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
    def _is_valid_ipv4_address(self, ip_address) -> bool:
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