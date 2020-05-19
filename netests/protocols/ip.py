#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from netests.constants import NOT_SET


class IPAddress(ABC):

    ip_address: str
    netmask: str

    def __init__(self, ip_address="0.0.0.0", netmask="0"):
        self.ip_address = ip_address

        if self.is_cidr_notation(netmask) is False:
            self.netmask = self.convert_netmask_to_cidr(netmask)
        else:
            self.netmask = netmask

    def __eq__(self, other):
        if not isinstance(other, IPAddress):
            return NotImplemented

        return (str(self.ip_address) == str(other.ip_address) and
                str(self.netmask) == str(other.netmask))

    def __repr__(self):
        return f"<{type(self)} ip_address={self.ip_address} " \
               f"netmask={self.netmask}>\n"

    @abstractmethod
    def _is_valid_ip_and_mask(self, ip_address, netmask) -> bool:
        pass

    @abstractmethod
    def _is_valid_netmask(self, netmask):
        pass

    @abstractmethod
    def _extract_ip_address(self, ip_address_with_netmask, separator="/") -> str:
        pass

    @abstractmethod
    def _extract_netmask(self, ip_address_with_netmask, separator="/") -> str:
        pass
