#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import *
from netests.protocols.ip import IPAddress

class Nexthop:

    ip_address: str
    is_in_fib: str
    out_interface: str
    preference: str  # or distance
    metric: str
    active: str

    def __init__(
        self,
        ip_address=NOT_SET,
        is_in_fib=NOT_SET,
        out_interface=NOT_SET,
        preference=NOT_SET,
        metric=NOT_SET,
        active=NOT_SET
    ):
        self.ip_address = ip_address
        self.is_in_fib = is_in_fib
        self.out_interface = out_interface
        self.preference = preference
        self.metric = metric
        self.active = active

    def __eq__(self, other):
        if not isinstance(other, Nexthop):
            return NotImplemented

        return (str(self.ip_address) == str(other.ip_address))

    def __repr__(self):
        return f"<Nexthop ip_address={self.ip_address} " \
               f"is_in_fib={self.is_in_fib} " \
               f"out_interface={self.out_interface} " \
               f"preference={self.preference} " \
               f"metric={self.metric} " \
               f"active={self.active}>\n"


class ListNexthop:

    nexthops_lst: list

    def __init__(self, nexthops_lst: list()):
        self.nexthops_lst = nexthops_lst

    def __eq__(self, others):
        if not isinstance(others, ListNexthop):
            print(type(others))
            raise NotImplemented

        for nexthop in self.nexthops_lst:
            if nexthop not in others.nexthops_lst:
                return False

        for nexthop in others.nexthops_lst:
            if nexthop not in self.nexthops_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListNexthop \n"
        for nexthop in self.nexthops_lst:
            result = result + f"{nexthop}"
        return result + ">"


class Static(IPAddress):

    vrf_name: str
    prefix: str
    netmask: str
    nexthop: ListNexthop

    def __init__(
        self,
        vrf_name=NOT_SET,
        prefix=NOT_SET,
        netmask=NOT_SET,
        nexthop=ListNexthop(list)
    ):
        self.vrf_name = vrf_name
        self.prefix = prefix

        if self.is_cidr_notation(netmask):
            if self.is_valid_cidr_netmask(netmask):
                self.netmask = self.convert_cidr_to_netmask(netmask)
            else:
                self.netmask = NOT_SET
        else:
            self.netmask = netmask

        self.nexthop = nexthop

    def __eq__(self, other):
        if not isinstance(other, Static):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)) and
                (str(self.prefix) == str(other.prefix)) and
                (str(self.netmask) == str(other.netmask)) and
                (self.nexthop == other.nexthop))

    def __repr__(self):
        return f"<Static vrf_name={self.vrf_name} " \
               f"prefix={self.prefix} " \
               f"netmask={self.netmask} " \
               f"nexthop={self.nexthop}>\n"


class ListStatic:

    static_routes_lst: list

    def __init__(self, static_routes_lst: list()):
        self.static_routes_lst = static_routes_lst

    def __eq__(self, others):
        if not isinstance(others, ListStatic):
            print(type(others))
            raise NotImplemented

        for static_route in self.static_routes_lst:
            if static_route not in others.static_routes_lst:
                return False

        for static_route in others.static_routes_lst:
            if static_route not in self.static_routes_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListStatic \n"
        for static_route in self.static_routes_lst:
            result = result + f"{static_route}"
        return result + ">"
