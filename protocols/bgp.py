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

######################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [bgp.py]"

######################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)
######################################################
#
# Class
#
class BGPSession:

    src_hostname: str
    dst_hostname: str
    src_interface: str

    # ------------------------------------------------------------
    #
    #
    def __init__(self, src_hostname: str(),  dst_hostname: str(), src_interface: str()):
        self.src_hostname = src_hostname
        self.dst_hostname = dst_hostname
        self.src_interface = src_interface

    # ------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplemented
    
        return ((self.src_hostname == other.src_hostname and
                self.dst_hostname == other.dst_hostname) and
                self.src_interface == other.src_interface)

    # ------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGPSession src_hostname={self.src_hostname} dst_hostname={self.dst_hostname} src_interface={self.src_interface}>\n"






class ListBGPSessions:

    bgp_sessions: list

    # ------------------------------------------------------------
    #
    #
    def __init__(self, bgp_sessions: list()):
        self.bgp_sessions = bgp_sessions

    # ------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListBGPSessions):
            raise NotImplemented

        for bgp_session in self.bgp_sessions:
            if bgp_session not in others.bgp_sessions:
                print(
                    f"[ListBGPSessions - __eq__] - The following BGP sessions is not in the list \n {bgp_session}")
                print(
                    f"[ListBGPSessions - __eq__] - List: \n {others.bgp_sessions}")
                return False

        for bgp_session in others.bgp_sessions:
            if bgp_session not in self.bgp_sessions:
                print(
                    f"[ListBGPSessions - __eq__] - The following BGP sessions is not in the list \n {bgp_session}")
                print(
                    f"[ListBGPSessions - __eq__] - List: \n {self.bgp_sessions}")
                return False

        return True

    # ------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListBGPSessions \n"
        for vrf_vni in self.bgp_sessions:
            result = result + f"{vrf_vni}"
        return result+"\n>"
