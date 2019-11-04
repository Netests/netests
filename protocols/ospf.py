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
ERROR_HEADER = "Error import [ospf.py]"

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
# OSPF SESSION CLASS
#
class OSPFSession:

    hostname: str
    peer_ip: str
    session_state: str

    # The following values are not used by the __eq__ function !!
    peer_hostname: str
    adjacency_time: str
    prefix_received: str

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, peer_ip=NOT_SET, session_state=NOT_SET, area=NOT_SET, peer_hostname=NOT_SET,
                 adjacency_time=NOT_SET, prefix_received=NOT_SET):
        self.hostname = hostname
        self.peer_ip = peer_ip
        self.session_state = session_state
        self.peer_hostname = peer_hostname
        self.adjacency_time = adjacency_time
        self.prefix_received = prefix_received

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, OSPFSession):
            return NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (str(self.peer_ip) == str(other.peer_ip)) and
                (str(self.session_state) == str(other.session_state)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<OSPFSession hostname={self.hostname} " \
               f"peer_ip={self.peer_ip} " \
               f"session_state={self.session_state} " \
               f"peer_hostname={self.peer_hostname} " \
               f"adjacency_time={self.adjacency_time} " \
               f"prefix_received={self.prefix_received}>\n"


########################################################################################################################
#
# OSPF SESSIONS LIST CLASS
#
class ListOSPFSessions:

    ospf_sessions_lst : list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ospf_sessions_lst: list()):
        self.ospf_sessions_lst = ospf_sessions_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessions):
            raise NotImplemented

        for ospf_session in self.ospf_sessions_lst:
            if ospf_session not in others.ospf_sessions_lst:
                print(
                    f"[ListOSPFSessions - __eq__] - The following OSPF sessions is not in the list \n {ospf_session}")
                print(
                    f"[ListOSPFSessions - __eq__] - List: \n {others.ospf_sessions_lst}")
                return False

        for ospf_session in others.ospf_sessions_lst:
            if ospf_session not in self.ospf_sessions_lst:
                print(
                    f"[ListOSPFSessions - __eq__] - The following OSPF sessions is not in the list \n {ospf_session}")
                print(
                    f"[ListOSPFSessions - __eq__] - List: \n {self.ospf_sessions_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListOSPFSessions \n"
        for ospf_session in self.ospf_sessions_lst:
            result = result + f"{ospf_session}"
        return result+">"


########################################################################################################################
#
# OSPF Sessions in a Area Class
#
class OSPFSessionsArea:

    area_number: str
    ospf_sessions: ListOSPFSessions

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, area_number: str, ospf_sessions=NOT_SET):
        self.area_number = area_number
        self.ospf_sessions = ospf_sessions

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, OSPFSessionsArea):
            raise NotImplemented

        return ((str(self.area_number) == str(other.area_number)) and
                 (self.ospf_sessions == other.ospf_sessions))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<OSPFSessionsArea area_number={self.area_number} " \
               f"ospf_sessions={self.ospf_sessions}>\n"



########################################################################################################################
#
# OSPF Sessions in a Area Class
#
class ListOSPFSessionsArea:

    ospf_sessions_area_lst: OSPFSessionsArea

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ospf_sessions_area_lst: list()):
        self.ospf_sessions_area_lst = ospf_sessions_area_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessionsArea):
            raise NotImplemented

        for ospf_session in self.ospf_sessions_area_lst:
            if ospf_session not in others.ospf_sessions_area_lst:
                print(
                    f"[ListOSPFSessionsArea - __eq__] - The following OSPF sessions is not in the list \n {ospf_session}")
                print(
                    f"[ListOSPFSessionsArea - __eq__] - List: \n {others.ospf_sessions_area_lst}")
                return False

        for ospf_session in others.ospf_sessions_area_lst:
            if ospf_session not in self.ospf_sessions_area_lst:
                print(
                    f"[ListOSPFSessionsArea - __eq__] - The following OSPF sessions is not in the list \n {ospf_session}")
                print(
                    f"[ListOSPFSessionsArea - __eq__] - List: \n {self.ospf_sessions_area_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListOSPFSessionsArea \n"
        for ospf_session in self.ospf_sessions_area_lst:
            result = result + f"{ospf_session}"
        return result + ">"


########################################################################################################################
#
# OSPF VRF CLASS
#
class OSPFSessionsVRF:

    vrf_name: str
    router_id: str
    ospf_sessions_area_lst: ListOSPFSessionsArea

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vrf_name: str, router_id=NOT_SET, ospf_sessions_area_lst=NOT_SET):
        self.vrf_name = vrf_name
        self.router_id = router_id
        self.ospf_sessions_area_lst = ospf_sessions_area_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, OSPFSessionsVRF):
            raise NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.router_id) == str(other.router_id)) and
                 (self.ospf_sessions_area_lst == other.ospf_sessions_area_lst))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<OSPFSessionsVRF vrf_name={self.vrf_name} " \
               f"router_id={self.router_id} " \
               f"ospf_sessions_area_lst={self.ospf_sessions_area_lst}>\n"


########################################################################################################################
#
# OSPF VRF List CLASS
#
class ListOSPFSessionsVRF:

    ospf_sessions_vrf_lst : list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, ospf_sessions_vrf_lst: list()):
        self.ospf_sessions_vrf_lst = ospf_sessions_vrf_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessionsVRF):
            raise NotImplemented

        for ospf_session_vrf in self.ospf_sessions_vrf_lst:
            if ospf_session_vrf not in others.ospf_sessions_vrf_lst:
                print(
                    f"[ListOSPFSessionsVRF - __eq__] The following OSPF sessions is not in the list \n {ospf_session_vrf}")
                print(
                    f"[ListOSPFSessionsVRF - __eq__] List: \n {others.ospf_sessions_vrf_lst}")
                return False

        for ospf_session_vrf in others.ospf_sessions_vrf_lst:
            if ospf_session_vrf not in self.ospf_sessions_vrf_lst:
                print(
                    f"[ListOSPFSessionsVRF - __eq__] The following OSPF sessions is not in the list \n {ospf_session_vrf}")
                print(
                    f"[ListOSPFSessionsVRF - __eq__] List: \n {self.ospf_sessions_vrf_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListOSPFSessionsVRF \n"
        for ospf_session_vrf in self.ospf_sessions_vrf_lst:
            result = result + f"{ospf_session_vrf}"
        return result + ">"


########################################################################################################################
#
# OSPF CLASS
#
class OSPF:

    hostname: str
    ospf_sessions_vrf_lst: ListOSPFSessionsVRF

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, hostname=NOT_SET, ospf_sessions_vrf_lst=NOT_SET):
        self.hostname = hostname
        self.ospf_sessions_vrf_lst = ospf_sessions_vrf_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, OSPF):
            raise NotImplemented

        return ((str(self.hostname) == str(other.hostname)) and
                (self.ospf_sessions_vrf_lst == other.ospf_sessions_vrf_lst))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<OSPF hostname={self.hostname} " \
                f"ospf_sessions_vrf_lst={self.ospf_sessions_vrf_lst}>"