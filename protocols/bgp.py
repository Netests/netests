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
    peer_ip: str
    peer_hostname: str

    # ------------------------------------------------------------
    #
    #
    def __init__(self, src_hostname=NOT_SET_VALUE, peer_ip=NOT_SET_VALUE, peer_hostname=NOT_SET_VALUE):
        self.src_hostname = src_hostname
        self.peer_ip = peer_ip
        self.peer_hostname = peer_hostname

    # ------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplemented

        return ((self.src_hostname == other.src_hostname) and
                (self.peer_ip == other.peer_ip) and
                (self.peer_hostname == other.peer_hostname))

    # ------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGPSession peer_ip={self.src_hostname} " \
               f"peer_ip={self.peer_ip} " \
               f"peer_hostname={self.peer_hostname}>\n "


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
