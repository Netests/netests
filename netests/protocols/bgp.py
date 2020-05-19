#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET

ERROR_HEADER = "Error import [bgp.py]"


class BGPSession:

    src_hostname: str
    peer_ip: str
    remote_as: str
    state_brief: str
    peer_hostname: str
    session_state: str
    state_time: str
    prefix_received: str
    options: dict

    def __init__(
        self,
        src_hostname=NOT_SET,
        peer_ip=NOT_SET,
        peer_hostname=NOT_SET,
        remote_as=NOT_SET,
        state_brief=NOT_SET,
        session_state=NOT_SET,
        state_time=NOT_SET,
        prefix_received=NOT_SET,
        options={}
    ):
        self.src_hostname = src_hostname
        self.peer_ip = peer_ip
        self.peer_hostname = peer_hostname
        self.remote_as = remote_as
        self.state_brief = state_brief
        self.session_state = session_state
        self.state_time = state_time
        self.prefix_received = prefix_received
        self.options = options

    def __eq__(self, other):
        if not isinstance(other, BGPSession):
            return NotImplementedError

        return (
            (str(self.src_hostname) == str(other.src_hostname)) and
            (str(self.peer_ip) == str(other.peer_ip)) and
            (str(self.state_brief) == str(other.state_brief)) and
            (str(self.remote_as) == str(other.remote_as))
        )

    def __repr__(self):
        return "<BGPSession" \
               f"\tsrc_hostname={self.src_hostname} " \
               f"\tpeer_ip={self.peer_ip} " \
               f"\tpeer_hostname={self.peer_hostname} " \
               f"\tremote_as={self.remote_as} " \
               f"\tstate_brief={self.state_brief} " \
               f"\tsession_state={self.session_state} "\
               f"\tstate_time={self.state_time} " \
               f"\tprefix_received={self.prefix_received}" \
               ">\n"

    def to_json(self):
        if 'print' in self.options.keys():
            r = dict()
            if self.options.get('print').get('src_hostname', True):
                r['src_hostname'] = self.src_hostname
            if self.options.get('print').get('peer_ip', True):
                r['peer_ip'] = self.peer_ip
            if self.options.get('print').get('peer_hostname', True):
                r['peer_hostname'] = self.peer_hostname
            if self.options.get('print').get('remote_as', True):
                r['remote_as'] = self.remote_as
            if self.options.get('print').get('state_brief', True):
                r['state_brief'] = self.state_brief
            if self.options.get('print').get('session_state', True):
                r['session_state'] = self.session_state
            if self.options.get('print').get('state_time', True):
                r['state_time'] = self.state_time
            if self.options.get('print').get('prefix_received', True):
                r['prefix_received'] = self.prefix_received
            return r
        else:
            return {
                "src_hostname": self.src_hostname,
                "peer_ip": self.peer_ip,
                "peer_hostname": self.peer_hostname,
                "remote_as": self.remote_as,
                "state_brief": self.state_brief,
                "session_state": self.session_state,
                "state_time": self.state_time,
                "prefix_received": self.prefix_received
            }


class ListBGPSessions:

    bgp_sessions: list

    def __init__(self, bgp_sessions: list()):
        self.bgp_sessions = bgp_sessions

    def __eq__(self, others):
        if not isinstance(others, ListBGPSessions):
            raise NotImplementedError

        for bgp_session in self.bgp_sessions:
            if bgp_session not in others.bgp_sessions:
                return False

        for bgp_session in others.bgp_sessions:
            if bgp_session not in self.bgp_sessions:
                return False

        return True

    def __repr__(self):
        result = "<ListBGPSessions \n"
        for bgp_session in self.bgp_sessions:
            result = result + f"{bgp_session}"
        return result+">"

    def to_json(self):
        data = list()
        for bgp in self.bgp_sessions:
            data.append(bgp.to_json())
        return data


class BGPSessionsVRF:

    vrf_name: str
    as_number: str
    router_id: str
    bgp_sessions: ListBGPSessions

    def __init__(
        self, vrf_name: str,
        as_number=NOT_SET,
        router_id=NOT_SET,
        bgp_sessions=NOT_SET
    ):
        self.vrf_name = vrf_name
        self.as_number = as_number
        self.router_id = router_id
        self.bgp_sessions = bgp_sessions

    def __eq__(self, other):
        if not isinstance(other, BGPSessionsVRF):
            raise NotImplementedError

        return (
            (str(self.vrf_name) == str(other.vrf_name)) and
            (str(self.as_number) == str(other.as_number)) and
            (str(self.router_id) == str(other.router_id)) and
            (self.bgp_sessions == other.bgp_sessions)
        )

    def __repr__(self):
        return "<BGPSessionsVRF" \
               f"\tvrf_name={self.vrf_name} " \
               f"\tas_number={self.as_number} " \
               f"\trouter_id={self.router_id} " \
               f"\tbgp_sessions={self.bgp_sessions}" \
                ">\n"

    def to_json(self):
        d = dict()
        d['as_number'] = self.as_number
        d['router_id'] = self.router_id
        d['neighbors'] = self.bgp_sessions.to_json()
        return d


class ListBGPSessionsVRF:

    bgp_sessions_vrf: list

    def __init__(self, bgp_sessions_vrf: list()):
        self.bgp_sessions_vrf = bgp_sessions_vrf

    def __eq__(self, others):
        if not isinstance(others, ListBGPSessionsVRF):
            raise NotImplementedError

        for bgp_session_vrf in self.bgp_sessions_vrf:
            if bgp_session_vrf not in others.bgp_sessions_vrf:
                return False

        for bgp_session_vrf in others.bgp_sessions_vrf:
            if bgp_session_vrf not in self.bgp_sessions_vrf:
                return False

        return True

    def __repr__(self):
        result = "<ListBGPSessionsVRF \n"
        for bgp_session_vrf in self.bgp_sessions_vrf:
            result = result + f"{bgp_session_vrf}"
        return result + ">"

    def to_json(self):
        data = list()
        for bgp in self.bgp_sessions_vrf:
            data.append(bgp.to_json())
        return data


class BGP:
    hostname: str
    bgp_sessions_vrf_lst: ListBGPSessionsVRF

    def __init__(self, hostname=NOT_SET, bgp_sessions_vrf_lst=NOT_SET):
        self.hostname = hostname
        self.bgp_sessions_vrf_lst = bgp_sessions_vrf_lst

    def __eq__(self, other):
        if not isinstance(other, BGP):
            raise NotImplementedError

        return (
            (str(self.hostname) == str(other.hostname)) and
            (self.bgp_sessions_vrf_lst == other.bgp_sessions_vrf_lst)
        )

    def __repr__(self):
        return f"<BGP hostname={self.hostname} " \
                f"bgp_sessions_vrf_lst={self.bgp_sessions_vrf_lst}>"

    def to_json(self):
        d = dict()
        for bgp in self.bgp_sessions_vrf_lst.bgp_sessions_vrf:
            d[bgp.vrf_name] = dict()
            d[bgp.vrf_name] = bgp.to_json()
        return d
