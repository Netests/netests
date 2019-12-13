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
ERROR_HEADER = "Error import [vlan.py]"

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
# VLAN CLASS
#
class VLAN:

    vlan_id: str
    vrf_name: str
    ip_address: str
    fhrp_ip_address: str
    netmask: str
    ports_members: list

    # The following values are not used by the __eq__ function !!
    vlan_name: str
    mac_address: str


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vlan_id=NOT_SET, vrf_name="default", ip_address=NOT_SET, fhrp_ip_address=NOT_SET,
                 netmask=NOT_SET, mac_address=NOT_SET, vlan_name=NOT_SET, ports_members=list()):

        self.vlan_id = vlan_id
        self.vrf_name = vrf_name
        self.ip_address = ip_address
        self.fhrp_ip_address = fhrp_ip_address
        self.netmask = netmask
        self.mac_address = mac_address
        self.vlan_name = vlan_name
        self.ports_members = ports_members

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, VLAN):
            return NotImplemented

        # Basic
        if (str(self.vlan_id) == str(self.vlan_id) and
                str(self.vrf_name) == str(other.vrf_name) and
                str(self.ip_address) == str(other.ip_address) and
                str(self.fhrp_ip_address) == str(other.fhrp_ip_address) and
                str(self.netmask) == str(other.netmask)):
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
        return f"<VLAN vlan_id={self.vlan_id} " \
               f"vrf_name={self.vrf_name} " \
               f"ip_address={self.ip_address} " \
               f"fhrp_ip_address={self.fhrp_ip_address} " \
               f"netmask={self.netmask} " \
               f"vlan_name={self.vlan_name} " \
               f"mac_address={self.mac_address} " \
               f"ports_members={self.ports_members}>\n"


########################################################################################################################
#
# VLAN LIST CLASS
#
class ListVLAN:

    vlans_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vlans_lst: list()):
        self.vlans_lst = vlans_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListVLAN):
            raise NotImplemented

        for vlan in self.vlans_lst:
            if vlan not in others.vlans_lst:
                print(
                    f"[ListVLAN - __eq__] - The following VLAN is not in the list \n {vlan}")
                print(
                    f"[ListVLAN - __eq__] - List: \n {others.vlans_lst}")
                return False

        for vlan in others.vlans_lst:
            if vlan not in self.vlans_lst:
                print(
                    f"[ListVLAN - __eq__] - The following VLAN is not in the list \n {vlan}")
                print(
                    f"[ListVLAN - __eq__] - List: \n {self.vlans_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListVLAN \n"
        for vlan in self.vlans_lst:
            result = result + f"{vlan}"
        return result + ">"