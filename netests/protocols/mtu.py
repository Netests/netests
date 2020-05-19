#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import *


class InterfaceMTU:

    interface_name: str
    mtu_size: str

    def __init__(self, interface_name=NOT_SET, mtu_size=NOT_SET):
        self.interface_name = interface_name
        self.mtu_size = mtu_size
		
    def __eq__(self, other):
        if not isinstance(other, InterfaceMTU):
            return NotImplemented

        return (
            (str(self.interface_name) == str(other.interface_name)) and
            (str(self.mtu_size) == str(other.mtu_size))
        )

    def __repr__(self):
        return f"\n<InterfaceMTU interface_name={self.interface_name} " \
               f"mtu_size={self.mtu_size}>"


class ListInterfaceMTU:

    interface_mtu_lst: list

    def __init__(self, interface_mtu_lst=list()):
        self.interface_mtu_lst = interface_mtu_lst

    def __eq__(self, other):
        if not isinstance(other, ListInterfaceMTU):
            return NotImplemented

        return (self.interface_mtu_lst == other.interface_mtu_lst)


    def __repr__(self):
        result = "<ListInterfaceMTU \n"
        for mtu in self.interface_mtu_lst:
            result = result + f"{mtu}"
        return result + ">"


class MTU:

    hostname: str
    mtu_global: str
    interface_mtu_lst: ListInterfaceMTU

    def __init__(
        self,
        hostname=NOT_SET,
        mtu_global=NOT_SET,
        interface_mtu_lst=list()
    ):
        self.hostname = hostname
        self.mtu_global = mtu_global
        self.interface_mtu_lst = interface_mtu_lst

    def __eq__(self, other):
        if not isinstance(other, MTU):
            return NotImplemented

        if self.mtu_global == NOT_SET:
            return (str(self.hostname) == str(other.hostname) and \
                    (self.interface_mtu_lst) == str(other.interface_mtu_lst))
        else:
            return (str(self.hostname) == str(other.hostname) and \
                    str(self.mtu_global) == str(other.mtu_global) and \
                    (self.interface_mtu_lst) == other.interface_mtu_lst)

    def __repr__(self):
        return f"<MTU \n" \
               f"hostname={self.hostname} \n" \
               f"<MTU mtu_global={self.mtu_global} \n" \
               f"interface_mtu_lst={self.interface_mtu_lst}>"
