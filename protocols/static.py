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
ERROR_HEADER = "Error import [static.py]"

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
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# STATIC ROUTE CLASS
#
class Static:

    vrf_name: str
    prefix: str
    netmask: str
    nexthop: str

    # The following values are not used by the __eq__ function !!
    is_in_fib: str
    out_interface: str
    preference: str # or distance
    metric: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vrf_name=NOT_SET, prefix=NOT_SET, netmask=NOT_SET, nexthop=NOT_SET, is_in_fib=NOT_SET,
                 out_interface=NOT_SET, preference=NOT_SET, metric=NOT_SET):
        self.vrf_name = vrf_name
        self.prefix = prefix

        if is_cidr_notation(netmask):
            if is_valid_cidr_netmask(netmask):
                self.netmask = convert_cidr_to_netmask(netmask)
            else:
                self.netmask = NOT_SET
        else:
            self.netmask = netmask

        self.nexthop = nexthop
        self.is_in_fib = is_in_fib
        self.out_interface = out_interface
        self.preference = preference
        self.metric = metric

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, Static):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.prefix) == str(other.prefix)) and
                (str(self.netmask) == str(other.netmask)) and
                (str(self.nexthop) == str(other.nexthop)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<Static vrf_name={self.vrf_name} " \
               f"prefix={self.prefix} " \
               f"netmask={self.netmask} " \
               f"nexthop={self.nexthop} " \
               f"is_in_fib={self.is_in_fib} " \
               f"out_interface={self.out_interface} "\
               f"preference={self.preference} " \
               f"metric={self.metric}>\n"

########################################################################################################################
#
# STATIC ROUTE LIST CLASS
#
class ListStatic:

    static_routes_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, static_routes_lst: list()):
        self.static_routes_lst = static_routes_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListStatic):
            print(type(others))
            raise NotImplemented

        for static_route in self.static_routes_lst:
            if static_route not in others.static_routes_lst:
                print(
                    f"[ListStatic - __eq__] - The following STATIC ROUTE is not in the list \n {static_route}")
                print(
                    f"[ListStatic - __eq__] - List: \n {others.static_routes_lst}")
                return False

        for static_route in others.static_routes_lst:
            if static_route not in self.static_routes_lst:
                print(
                    f"[ListStatic - __eq__] - The following STATIC ROUTE is not in the list \n {static_route}")
                print(
                    f"[ListStatic - __eq__] - List: \n {self.static_routes_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListStatic \n"
        for static_route in self.static_routes_lst:
            result = result + f"{static_route}"
        return result + ">"