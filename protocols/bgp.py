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

########################################################################################################################
#
# BGP SESSION CLASS
#
class BGPSession:

    src_hostname: str
    peer_ip: str
    peer_hostname: str
    remote_as: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, src_hostname=NOT_SET, peer_ip=NOT_SET, peer_hostname=NOT_SET,remote_as=NOT_SET):
        self.src_hostname = src_hostname
        self.peer_ip = peer_ip
        self.peer_hostname = peer_hostname
        self.remote_as = remote_as

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplemented

        return ((self.src_hostname == other.src_hostname) and
                (self.peer_ip == other.peer_ip) and
                (self.peer_hostname == other.peer_hostname) and
                (self.remote_as == other.remote_as))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGPSession src_hostname={self.src_hostname} " \
               f"peer_ip={self.peer_ip} " \
               f"peer_hostname={self.peer_hostname} " \
               f"remote_as={self.remote_as}>\n"


########################################################################################################################
#
# BGP SESSIONS LIST CLASS
#
class ListBGPSessions:

    bgp_sessions: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, bgp_sessions: list()):
        self.bgp_sessions = bgp_sessions

    # ------------------------------------------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListBGPSessions \n"
        for bgp_session in self.bgp_sessions:
            result = result + f"{bgp_session}"
        return result+"\n>"


########################################################################################################################
#
# BGP CLASS
#
class BGP:

    hostname: str
    as_number: str
    router_id: str
    bgp_sessions: ListBGPSessions

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, as_number=NOT_SET, router_id=NOT_SET, bgp_sessions=NOT_SET):
        self.hostname = hostname
        self.as_number = as_number
        self.router_id = router_id
        self.bgp_sessions = bgp_sessions

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGP):
            raise NotImplemented

        return ((self.hostname == other.hostname) and
                (self.as_number == other.as_number) and
                (self.router_id == other.router_id) and
                (self.bgp_sessions == other.bgp_sessions))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGP hostname={self.hostname} " \
               f"as_number={self.as_number} " \
               f"router_id={self.router_id} " \
               f"bgp_sessions={self.bgp_sessions}>\n "