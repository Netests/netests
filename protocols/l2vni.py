#/usr/bin/env python3.7
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
ERROR_HEADER = "Error import [l2vni.py]"

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
# L2VNI CLASS
#
class L2VNI:

    vxlan_int: str
    vtep_ip: str
    vni: str
    vrf: str
    multicast_gr_ip: str

    # The following values are not used by the __eq__ function !!
    remote_vteps: list


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vxlan_int=NOT_SET, vtep_ip="0.0.0.0", vni=NOT_SET,
                 vrf=NOT_SET,remote_vteps=NOT_SET, multicast_gr_ip="0.0.0.0"):

        self.vxlan_int = vxlan_int
        self.vtep_ip = vtep_ip
        self.vni = vni
        self.vrf = vrf
        self.remote_vteps = remote_vteps
        self.multicast_gr_ip = multicast_gr_ip

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, L2VNI):
            return NotImplemented

        # Basic
        if (str(self.vxlan_int) == str(self.vxlan_int) and
                str(self.vtep_ip) == str(other.vtep_ip) and
                str(self.vni) == str(other.vni) and
                str(self.vrf) == str(other.vrf) and
                str(self.multicast_gr_ip) == str(other.multicast_gr_ip)):
            return True

        else:
            printline()
            print(self)
            print("IS NOT EQUAL TO\n")
            print(other)
            printline()
            return False

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<L2VNI vxlan_int={self.vxlan_int} " \
               f"vtep_ip={self.vtep_ip} " \
               f"vni={self.vni} " \
               f"vrf={self.vrf} " \
               f"multicast_gr_ip={self.multicast_gr_ip} " \
               f"remote_vteps={self.remote_vteps}>\n"


########################################################################################################################
#
# CDP LIST CLASS
#
class ListL2VNI:

    l2vni_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, l2vni_lst: list()):
        self.l2vni_lst = l2vni_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListL2VNI):
            raise NotImplemented

        for l2vni in self.l2vni_lst:
            if l2vni not in others.l2vni_lst:
                print(
                    f"[ListL2VNI - __eq__] - The following L2VNI is not in the list \n {l2vni}")
                print(
                    f"[ListL2VNI - __eq__] - List: \n {others.l2vni_lst}")
                return False

        for l2vni in others.l2vni_lst:
            if l2vni not in self.l2vni_lst:
                print(
                    f"[ListL2VNI - __eq__] - The following L2VNI is not in the list \n {l2vni}")
                print(
                    f"[ListL2VNI - __eq__] - List: \n {self.l2vni_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListL2VNI \n"
        for l2vni in self.l2vni_lst:
            result = result + f"{l2vni}"
        return result + ">"