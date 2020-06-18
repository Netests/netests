#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from typing import Union
from ipaddress import IPv4Address, IPv6Address
from netests.protocols._protocols import NetestsProtocol
from netests.constants import COMPARE_OPTION_KEY, PRINT_OPTION_KEY


class IPAddress(NetestsProtocol):
    ip_address: Union[IPv4Address, IPv6Address] = None
    netmask: str = None

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            raise NotImplementedError()

        if COMPARE_OPTION_KEY in self.options.keys():
            log.debug(f"Compare modified function\noptions={self.options}")
            is_equal = True
            if self.options.get(COMPARE_OPTION_KEY).get('ip_address', True):
                if self.ip_address != other.ip_address:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('netmask', True):
                if self.netmask != other.netmask:
                    is_equal = False
            return is_equal
        else:
            return (
                self.ip_address == other.ip_address and
                self.netmask == other.netmask
            )

    def to_json(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = dict()
            if self.options.get(PRINT_OPTION_KEY).get('ip_address', True):
                ret['ip_address'] = self.ip_address
            if self.options.get(PRINT_OPTION_KEY).get('netmask', True):
                ret['netmask'] = self.netmask
            return ret
        else:
            return {
                "ip_address": self.ip_address,
                "netmask": self.netmask
            }

    def __repr__(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = f"<{type(self)}\n"
            if self.options.get(PRINT_OPTION_KEY).get('ip_address', True):
                ret += f"\tip_address={self.ip_address}\n"
            if self.options.get(PRINT_OPTION_KEY).get('netmask', True):
                ret += f"\tnetmask={self.netmask}\n"
            return ret + ">\n"
        else:
            return str(
                f"<{type(self)}\n"
                f"\tip_address={self.ip_address}\n"
                f"\tnetmask={self.netmask}\n>"
            )
