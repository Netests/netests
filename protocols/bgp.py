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
ERROR_HEADER = "Error import [bgp.py]"

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

########################################################################################################################
#
# BGP SESSION CLASS
#
class BGPSession:

    src_hostname: str
    peer_ip: str
    remote_as: str

    # The following values are not used by the __eq__ function !!
    state_brief: str
    peer_hostname: str
    session_state: str
    state_time: str
    prefix_received: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, src_hostname=NOT_SET, peer_ip=NOT_SET, peer_hostname=NOT_SET, remote_as=NOT_SET,
                 state_brief=NOT_SET, session_state=NOT_SET, state_time=NOT_SET, prefix_received=NOT_SET):
        self.src_hostname = src_hostname
        self.peer_ip = peer_ip
        self.peer_hostname = peer_hostname
        self.remote_as = remote_as
        self.state_brief = state_brief
        self.session_state = session_state
        self.state_time = state_time
        self.prefix_received = prefix_received

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplemented

        return ((str(self.src_hostname) == str(other.src_hostname)) and
                (str(self.peer_ip) == str(other.peer_ip)) and
                (str(self.state_brief) == str(other.state_brief)) and
                (str(self.remote_as) == str(other.remote_as)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGPSession src_hostname={self.src_hostname} " \
               f"peer_ip={self.peer_ip} " \
               f"peer_hostname={self.peer_hostname} " \
               f"remote_as={self.remote_as} " \
               f"state_brief={self.state_brief} " \
               f"session_state={self.session_state} "\
               f"state_time={self.state_time} " \
               f"prefix_received={self.prefix_received}>\n"


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
        return result+">"


########################################################################################################################
#
# BGP VRF CLASS
#
class BGPSessionsVRF:

    vrf_name: str
    as_number: str
    router_id: str
    bgp_sessions: ListBGPSessions


    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vrf_name: str, as_number=NOT_SET, router_id=NOT_SET, bgp_sessions=NOT_SET):
        self.vrf_name = vrf_name
        self.as_number = as_number
        self.router_id = router_id
        self.bgp_sessions = bgp_sessions

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGPSessionsVRF):
            raise NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.as_number) == str(other.as_number)) and
                (str(self.router_id) == str(other.router_id)) and
                 (self.bgp_sessions == other.bgp_sessions))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGPSessionsVRF vrf_name={self.vrf_name} " \
               f"as_number={self.as_number} " \
               f"router_id={self.router_id} " \
               f"bgp_sessions={self.bgp_sessions}>\n"


########################################################################################################################
#
# BGP VRF CLASS
#
class ListBGPSessionsVRF:

    bgp_sessions_vrf: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, bgp_sessions_vrf: list()):
        self.bgp_sessions_vrf = bgp_sessions_vrf

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListBGPSessionsVRF):
            raise NotImplemented

        for bgp_session_vrf in self.bgp_sessions_vrf:
            if bgp_session_vrf not in others.bgp_sessions_vrf:
                print(
                    f"[ListBGPSessionsVRF - __eq__] The following BGP sessions is not in the list \n {bgp_session_vrf}")
                print(
                    f"[ListBGPSessionsVRF - __eq__] List: \n {others.bgp_sessions_vrf}")
                return False

        for bgp_session_vrf in others.bgp_sessions_vrf:
            if bgp_session_vrf not in self.bgp_sessions_vrf:
                print(
                    f"[ListBGPSessionsVRF - __eq__] The following BGP sessions is not in the list \n {bgp_session_vrf}")
                print(
                    f"[ListBGPSessionsVRF - __eq__] List: \n {self.bgp_sessions_vrf}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListBGPSessionsVRF \n"
        for bgp_session_vrf in self.bgp_sessions_vrf:
            result = result + f"{bgp_session_vrf}"
        return result + ">"


########################################################################################################################
#
# BGP CLASS
#
class BGP:

    hostname: str
    bgp_sessions_vrf_lst: ListBGPSessionsVRF

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, bgp_sessions_vrf_lst=NOT_SET):
        self.hostname = hostname
        self.bgp_sessions_vrf_lst = bgp_sessions_vrf_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, BGP):
            raise NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (self.bgp_sessions_vrf_lst == other.bgp_sessions_vrf_lst))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<BGP hostname={self.hostname} " \
                f"bgp_sessions_vrf_lst={self.bgp_sessions_vrf_lst}>"