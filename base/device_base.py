#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Abstract class that have to be implement by each devices.

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

######################################################
#
# Default value used for exit()
#
EXIT_SUCCESS = 0
EXIT_FAILURE = 1


######################################################
#
# Import Library
#
try:
    from abc import ABC, abstractmethod
except ImportError as importError:
    print("Error import [device_base] abc")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import protocols.bgp
except ImportError as importError:
    print("Error import [device_base] bgp")
    print(importError)
    exit(EXIT_FAILURE)


class DeviceBase(ABC):

    def ssh_connexion():
        pass

    def create_bgp_obj(local_peer: str(), remote_peer: str(), interface) -> BGPSession():
        pass

    @abstractmethod
    def get_bgp_information():
        pass

    