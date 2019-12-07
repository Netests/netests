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
ERROR_HEADER = "Error import [mtu.py]"

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
# Interface MTU CLASS
#
class InterfaceMTU:

    interface_name: str
    mtu_size: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, interface_name=NOT_SET, mtu_size=NOT_SET):
        self.interface_name = interface_name
        self.mtu_size = mtu_size
		
    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, InterfaceMTU):
            return NotImplemented

        return ((str(self.interface_name) == str(other.interface_name)) and
                (str(self.mtu_size) == str(other.mtu_size)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"\n<InterfaceMTU interface_name={self.interface_name} " \
               f"mtu_size={self.mtu_size}>"


			   
########################################################################################################################
#
# List Interface MTU CLASS
#
class ListInterfaceMTU:

    interface_mtu_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, interface_mtu_lst=list()):
        self.interface_mtu_lst = interface_mtu_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, ListInterfaceMTU):
            return NotImplemented

        return (self.interface_mtu_lst == other.interface_mtu_lst)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListInterfaceMTU \n"
        for mtu in self.interface_mtu_lst:
            result = result + f"{mtu}"
        return result + ">"

########################################################################################################################
#
# MTU CLASS
#
class MTU:

    hostname: str
    mtu_global: str
    interface_mtu_lst: ListInterfaceMTU

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, mtu_global=NOT_SET, interface_mtu_lst=list()):
        self.hostname = hostname
        self.mtu_global = mtu_global
        self.interface_mtu_lst = interface_mtu_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, MTU):
            return NotImplemented

        if self.mtu_global == NOT_SET:
            return (str(self.hostname) == str(other.hostname) and \
                    (self.interface_mtu_lst) == str(other.interface_mtu_lst))
        else:
            return (str(self.hostname) == str(other.hostname) and \
                    str(self.mtu_global) == str(other.mtu_global) and \
                    (self.interface_mtu_lst) == other.interface_mtu_lst)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<MTU \n" \
               f"hostname={self.hostname} \n" \
               f"<MTU mtu_global={self.mtu_global} \n" \
               f"interface_mtu_lst={self.interface_mtu_lst}>"