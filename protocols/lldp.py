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
ERROR_HEADER = "Error import [lldp.py]"

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
    from protocols.discovery_protocols import DiscoveryProtocols
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.discovery_protocols")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# LLDP NEIGHBORS CLASS
#
class LLDP(DiscoveryProtocols):

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, local_name=NOT_SET, local_port=NOT_SET,neighbor_name=NOT_SET, neighbor_port=NOT_SET,
                 neighbor_os=NOT_SET, neighbor_mgmt_ip=NOT_SET, neighbor_type=list()):
        super(LLDP, self).__init__(local_name, local_port, neighbor_name, neighbor_port,
                                   neighbor_os, neighbor_mgmt_ip, neighbor_type)
    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, LLDP):
            return NotImplemented

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port) or (
                self.local_name == other.neighbor_name and
                self.local_port == other.neighbor_port and
                self.neighbor_name == other.local_name and
                self.neighbor_port == other.local_port)

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return super(LLDP, self).__repr__()


########################################################################################################################
#
# LLDP LIST CLASS
#
class ListLLDP:

    lldp_neighbors_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, lldp_neighbors_lst: list()):
        self.lldp_neighbors_lst = lldp_neighbors_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListLLDP):
            raise NotImplemented

        for lldp in self.lldp_neighbors_lst:
            if lldp not in others.lldp_neighbors_lst:
                print(
                    f"[ListLLDP - __eq__] - The following LLDP session is not in the list \n {lldp}")
                print(
                    f"[ListLLDP - __eq__] - List: \n {others.lldp_neighbors_lst}")
                return False

        for lldp in others.lldp_neighbors_lst:
            if lldp not in self.lldp_neighbors_lst:
                print(
                    f"[ListLLDP - __eq__] - The following LLDP session is not in the list \n {lldp}")
                print(
                    f"[ListLLDP - __eq__] - List: \n {self.lldp_neighbors_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListLLDP \n"
        for lldp in self.lldp_neighbors_lst:
            result = result + f"{lldp}"
        return result + ">"