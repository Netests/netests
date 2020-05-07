#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import NOT_SET


ERROR_HEADER = "Error import [ping.py]"


class PING:

    src_host: str
    ip_address: str
    vrf:  str

    def __init__(self, src_host= NOT_SET, ip_address=NOT_SET, vrf=NOT_SET):
        self.src_host = src_host
        self.ip_address = ip_address
        self.vrf = vrf

    def __eq__(self, other):
        if not isinstance(other, PING):
            return NotImplemented

        return ((str(self.ip_address) == str(other.ip_address)) and
                (str(self.src_host) == str(other.src_host)) and
                (str(self.vrf) == str(other.vrf)))

    def __repr__(self):
        return f"<PING src_host={self.src_host} " \
               f"ip_address={self.ip_address} " \
               f"vrf={self.vrf}>\n"
               
    def to_json(self):
        return {
            "src_host": self.src_host,
            "ip_address": self.ip_address,
            "vrf": self.vrf
        }


class ListPING:

    ping_lst: list

    def __init__(self, ping_lst: list()):
        self.ping_lst = ping_lst

    def __eq__(self, others):
        if not isinstance(others, ListPING):
            raise NotImplemented

        for ping in self.ping_lst:
            if ping not in others.ping_lst:
                return False

        for ping in others.ping_lst:
            if ping not in self.ping_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListPING \n"
        for ping in self.ping_lst:
            result = result + f"{ping}"
        return result + ">"

    def to_json(self):
        l = list()
        for p in self.ping_lst:
            l.append(p.to_json())
        return l
