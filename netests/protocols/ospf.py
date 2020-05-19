#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET


ERROR_HEADER = "Error import [ospf.py]"


class OSPFSession:

    hostname: str
    peer_rid: str
    local_interface: str
    peer_ip: str
    session_state: str
    peer_hostname: str

    def __init__(
        self,
        peer_rid=NOT_SET,
        session_state=NOT_SET,
        peer_hostname=NOT_SET,
        local_interface=NOT_SET,
        peer_ip=NOT_SET,
        options={}
    ):
        self.peer_rid = peer_rid
        self.session_state = str(session_state).upper()
        self.peer_hostname = peer_hostname
        self.local_interface = local_interface
        self.peer_ip = peer_ip
        self.options = options

    def __eq__(self, other):
        if not isinstance(other, OSPFSession):
            return NotImplemented

        return (
                (str(self.local_interface) == str(other.local_interface)) and
                (str(self.peer_rid) == str(other.peer_rid))
        )

    def __repr__(self):
        return f"<OSPFSession " \
               f"peer_rid={self.peer_rid} " \
               f"session_state={self.session_state} " \
               f"peer_hostname={self.peer_hostname} " \
               f"local_interface={self.local_interface} " \
               f"peer_ip={self.peer_ip}>\n"

    def to_json(self):
        return {
            "peer_rid": self.peer_rid,
            "session_state": self.session_state,
            "peer_hostname": self.peer_hostname,
            "local_interface": self.local_interface,
            "peer_ip": self.peer_ip,
        }


class ListOSPFSessions:

    ospf_sessions_lst: list

    def __init__(self, ospf_sessions_lst: list()):
        self.ospf_sessions_lst = ospf_sessions_lst

    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessions):
            raise NotImplementedError()

        for ospf_session in self.ospf_sessions_lst:
            if ospf_session not in others.ospf_sessions_lst:
                return False

        for ospf_session in others.ospf_sessions_lst:
            if ospf_session not in self.ospf_sessions_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListOSPFSessions \n"
        for ospf_session in self.ospf_sessions_lst:
            result = result + f"{ospf_session}"
        return result+">"

    def to_json(self):
        data = list()
        for ospf in self.ospf_sessions_lst:
            data.append(ospf.to_json())
        return data


class OSPFSessionsArea:

    area_number: str
    ospf_sessions: ListOSPFSessions

    def __init__(self, area_number: str, ospf_sessions=NOT_SET):
        self.area_number = area_number
        self.ospf_sessions = ospf_sessions

    def __eq__(self, other):
        if not isinstance(other, OSPFSessionsArea):
            raise NotImplementedError()

        return ((str(self.area_number) == str(other.area_number)) and
                (self.ospf_sessions == other.ospf_sessions))

    def __repr__(self):
        return f"<OSPFSessionsArea area_number={self.area_number} " \
               f"ospf_sessions={self.ospf_sessions}>\n"

    def to_json(self):
        d = dict()
        d['area_number'] = self.area_number
        d['neighbors'] = self.ospf_sessions.to_json()
        return d


class ListOSPFSessionsArea:

    ospf_sessions_area_lst: list

    def __init__(self, ospf_sessions_area_lst: list()):
        self.ospf_sessions_area_lst = ospf_sessions_area_lst

    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessionsArea):
            raise NotImplementedError()

        if (
            len(self.ospf_sessions_area_lst) !=
            len(others.ospf_sessions_area_lst)
        ):
            return False

        for ospf_session in self.ospf_sessions_area_lst:
            if ospf_session not in others.ospf_sessions_area_lst:
                return False

        for ospf_session in others.ospf_sessions_area_lst:
            if ospf_session not in self.ospf_sessions_area_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListOSPFSessionsArea \n"
        for ospf_session in self.ospf_sessions_area_lst:
            result = result + f"{ospf_session}"
        return result + ">"

    def to_json(self):
        data = list()
        for ospf in self.ospf_sessions_area_lst:
            data.append(ospf.to_json())
        return data


class OSPFSessionsVRF:

    vrf_name: str
    router_id: str
    ospf_sessions_area_lst: ListOSPFSessionsArea

    def __init__(
        self,
        vrf_name=NOT_SET,
        router_id=NOT_SET,
        ospf_sessions_area_lst=ListOSPFSessionsArea(
            ospf_sessions_area_lst=list()
        )
    ):
        self.vrf_name = vrf_name
        self.router_id = router_id
        self.ospf_sessions_area_lst = ospf_sessions_area_lst

    def __eq__(self, other):
        if not isinstance(other, OSPFSessionsVRF):
            raise NotImplementedError()

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.router_id) == str(other.router_id)) and
                (self.ospf_sessions_area_lst == other.ospf_sessions_area_lst))

    def __repr__(self):
        return f"<OSPFSessionsVRF vrf_name={self.vrf_name} " \
               f"router_id={self.router_id} " \
               f"ospf_sessions_area_lst={self.ospf_sessions_area_lst}>\n"

    def to_json(self):
        d = dict()
        d['vrf_name'] = self.vrf_name
        d['router_id'] = self.router_id
        d['areas'] = self.ospf_sessions_area_lst.to_json()
        return d


class ListOSPFSessionsVRF:

    ospf_sessions_vrf_lst: list

    def __init__(self, ospf_sessions_vrf_lst: list()):
        self.ospf_sessions_vrf_lst = ospf_sessions_vrf_lst

    def __eq__(self, others):
        if not isinstance(others, ListOSPFSessionsVRF):
            raise NotImplementedError()

        for ospf_session_vrf in self.ospf_sessions_vrf_lst:
            if ospf_session_vrf not in others.ospf_sessions_vrf_lst:
                return False

        for ospf_session_vrf in others.ospf_sessions_vrf_lst:
            if ospf_session_vrf not in self.ospf_sessions_vrf_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListOSPFSessionsVRF \n"
        for ospf_session_vrf in self.ospf_sessions_vrf_lst:
            result = result + f"{ospf_session_vrf}"
        return result + ">"

    def to_json(self):
        data = list()
        for ospf in self.ospf_sessions_vrf_lst:
            data.append(ospf.to_json())
        return data


class OSPF:

    hostname: str
    ospf_sessions_vrf_lst: ListOSPFSessionsVRF

    def __init__(self, hostname=NOT_SET, ospf_sessions_vrf_lst=NOT_SET):
        self.hostname = hostname
        self.ospf_sessions_vrf_lst = ospf_sessions_vrf_lst

    def __eq__(self, other):
        if not isinstance(other, OSPF):
            raise NotImplementedError()

        return ((str(self.hostname) == str(other.hostname)) and
                (self.ospf_sessions_vrf_lst == other.ospf_sessions_vrf_lst))

    def __repr__(self):
        return f"<OSPF hostname={self.hostname} " \
                f"ospf_sessions_vrf_lst={self.ospf_sessions_vrf_lst}>"

    def to_json(self):
        d = dict()
        d['hostname'] = self.hostname
        d['vrfs'] = self.ospf_sessions_vrf_lst.to_json()
        return d
