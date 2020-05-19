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
ERROR_HEADER = "Error import [bond.py]"

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
# BOND CLASS
#
class BOND:

    bond_name: str
    ports_members: list
    vlans_members: list
    native_vlan: str

    # The following values are not used by the __eq__ function !!
    mode: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, bond_name=NOT_SET, ports_members=list, vlans_members=list, native_vlan=NOT_SET, mode=NOT_SET):

        self.bond_name = bond_name
        self.ports_members = ports_members
        self.vlans_members = vlans_members
        self.native_vlan = native_vlan
        self.mode = mode

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BOND):
            return NotImplemented

        return (str(self.bond_name) == str(other.bond_name) and
                (self.ports_members == other.ports_members) and
                (self.vlans_members == other.vlans_members) and
                (str(self.native_vlan) == str(other.native_vlan)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BOND bond_name={self.bond_name} \n" \
               f"ports_members={self.ports_members} \n" \
               f"vlans_members={self.vlans_members} \n" \
               f"native_vlan={self.native_vlan} \n" \
               f"mode={self.mode}>\n --- \n" \

########################################################################################################################
#
# BOND LIST CLASS
#
class ListBOND:

    bonds_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, bonds_lst: list()):
        self.bonds_lst = bonds_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListBOND):
            raise NotImplemented

        for bond in self.bonds_lst:
            if bond not in others.bonds_lst:
                print(
                    f"[ListBOND - __eq__] - The following BOND is not in the list \n {bond}")
                print(
                    f"[ListBOND - __eq__] - List: \n {others.bonds_lst}")
                return False

        for bond in others.bonds_lst:
            if bond not in self.bonds_lst:
                print(
                    f"[ListBOND - __eq__] - The following BOND is not in the list \n {bond}")
                print(
                    f"[ListBOND - __eq__] - List: \n {self.bonds_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListBOND \n"
        for bond in self.bonds_lst:
            result = result + f"{bond}"
        return result + ">"