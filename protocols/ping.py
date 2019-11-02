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
ERROR_HEADER = "Error import [ping.py]"

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

########################################################################################################################
#
# VRF CLASS
#
class PING:

    src_host: str
    ip_address: str
    vrf:  str


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, src_host= NOT_SET, ip_address=NOT_SET, vrf="default"):
        self.src_host = src_host
        self.ip_address = ip_address
        self.vrf = vrf
    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, PING):
            return NotImplemented

        return ((str(self.ip_address) == str(other.ip_address)) and
                (str(self.src_host) == str(other.src_host)) and
                (str(self.vrf) == str(other.vrf)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<PING src_host={self.src_host} " \
               f"ip_address={self.ip_address} " \
               f"vrf={self.vrf}>\n"


########################################################################################################################
#
# PING LIST CLASS
#
class ListPING:

    ping_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ping_lst: list()):
        self.ping_lst = ping_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListPING):
            raise NotImplemented

        for ping in self.ping_lst:
            if ping not in others.ping_lst:
                print(
                    f"[ListPING - __eq__] - The following PING is not in the list \n {ping}")
                print(
                    f"[ListPING - __eq__] - List: \n {others.ping_lst}")
                return False

        for ping in others.ping_lst:
            if ping not in self.ping_lst:
                print(
                    f"[ListPING - __eq__] - The following PING is not in the list \n {ping}")
                print(
                    f"[ListPING - __eq__] - List: \n {self.ping_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListPING \n"
        for ping in self.ping_lst:
            result = result + f"{ping}"
        return result + ">"