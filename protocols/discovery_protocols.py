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
ERROR_HEADER = "Error import [discovery_protocols.py]"

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
class DiscoveryProtocols(ABC):

    local_name: str
    local_port: str
    neighbor_name: str
    neighbor_port: str

    # Following parameter is not use in compare function
    neighbor_os:str
    neighbor_mgmt_ip: str
    neighbor_type: list


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, local_name=NOT_SET, local_port=NOT_SET, neighbor_name=NOT_SET, neighbor_port=NOT_SET,
                 neighbor_os=NOT_SET, neighbor_mgmt_ip=NOT_SET, neighbor_type=list()):
        self.local_name = local_name
        self.local_port = local_port
        self.neighbor_name = neighbor_name
        self.neighbor_port = neighbor_port
        self.neighbor_os = neighbor_os
        self.neighbor_mgmt_ip = neighbor_mgmt_ip
        self.neighbor_type = neighbor_type


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, DiscoveryProtocols):
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
        return f"<{type(self)} local_name={self.local_name}\n" \
               f"local_port={self.local_port}\n" \
               f"neighbor_mgmt_ip={self.neighbor_mgmt_ip}\n" \
               f"neighbor_name={self.neighbor_name}\n" \
               f"neighbor_port={self.neighbor_port}\n" \
               f"neighbor_os={self.neighbor_os}\n" \
               f"neighbor_type={self.neighbor_type}>\n"