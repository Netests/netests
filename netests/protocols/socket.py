#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import *


class SOCKET:

    ip: str
    port: str
    timeout: str
    vrf: str
    protocol: str
    work: str

    def __init__(
        self,
        ip= NOT_SET,
        port=NOT_SET,
        timeout=1,
        vrf="default",
        protocol="tcp",
        work=True
    ):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.vrf = vrf
        self.protocol = protocol
        self.work = work

    def __eq__(self, other):
        if not isinstance(other, SOCKET):
            return NotImplemented

        return ((str(self.ip) == str(other.ip)) and
                (str(self.port) == str(other.port)) and
                (str(self.timeout) == str(other.timeout)) and
                (str(self.vrf) == str(other.vrf)) and
                (str(self.protocol) == str(other.protocol)) and
                (str(self.work) == str(other.work)))

    def __repr__(self):
        return f"<SOCKET ip={self.ip} " \
               f"port={self.port} " \
               f"timeout={self.timeout} " \
               f"vrf={self.vrf} " \
               f"protocol={self.protocol} " \
               f"work={self.work}>\n"


class ListSOCKET:

    socket_lst: list

    def __init__(self, socket_lst: list()):
        self.socket_lst = socket_lst

    def __eq__(self, others):
        if not isinstance(others, ListSOCKET):
            raise NotImplemented

        for socket in self.socket_lst:
            if socket not in others.socket_lst:
                return False

        for socket in others.socket_lst:
            if socket not in self.socket_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListSOCKET \n"
        for socket in self.socket_lst:
            result = result + f"{socket}"
        return result + ">"
