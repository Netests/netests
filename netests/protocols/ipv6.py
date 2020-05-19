#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from netests.constants import NOT_SET
from netests.protocols.ip import IPAddress


class IPV6(IPAddress):

    def __init__(self, ip_address_with_mask=NOT_SET, netmask=NOT_SET):
        if NOT_SET == netmask:
            index_slash = str(ip_address_with_mask).find("/")

            super().__init__(
                ip_address=ip_address_with_mask[:index_slash],
                netmask=ip_address_with_mask[index_slash+1:]
            )
        else:
            super().__init__(
                ip_address=ip_address_with_mask,
                netmask=netmask
            )

    def _is_valid_ip_and_mask(self, ip_address, netmask) -> bool:
        pass

    def _is_valid_ipv6_address(self, ip_address) -> bool:
        pass

    def _is_valid_netmask(self, netmask):
        pass

    def _extract_ip_address(self, ip_address_with_netmask, separator="/") -> str:
        pass

    def _extract_netmask(self, ip_address_with_netmask, separator="/") -> str:
        pass


class ListIPV6:

    ipv6_addresses_lst: list

    def __init__(self, ipv6_addresses_lst: list()):
        self.ipv6_addresses_lst = ipv6_addresses_lst

    def __eq__(self, others):
        if not isinstance(others, ListIPV6):
            raise NotImplemented

        for ipv6 in self.ipv6_addresses_lst:
            if ipv6 not in others.ipv6_addresses_lst:
                return False

        for ipv6 in others.ipv6_addresses_lst:
            if ipv6 not in self.ipv6_addresses_lst:
                return False

        return True

    def __repr__(self):
        result = f"<ListIPV6 \n"
        for ipv6 in self.ipv6_addresses_lst:
            result = result + f"{ipv6}"
        return result + ">"


class IPV6Interface(IPV6):

    interface_name: str

    def __init__(
        self,
        interface_name=NOT_SET,
        ip_address_with_mask=NOT_SET,
        netmask=NOT_SET
    ):
        self.interface_name = interface_name
        super().__init__(ip_address_with_mask, netmask)

    def __eq__(self, other):
        if not isinstance(other, IPV6Interface):
            return NotImplemented

        return (str(self.ip_address) == str(other.ip_address) and
                str(self.netmask) == str(other.netmask) and
                str(self.interface_name) == str(other.interface_name))

    def __repr__(self):
        return f"<{type(self)} ip_address={self.ip_address} " \
               f"netmask={self.netmask} " \
               f"interface_name={self.interface_name}>\n"

class ListIPV6Interface():

    ipv6_addresses_lst: list

    def __init__(self, ipv6_addresses_lst: list()):
        self.ipv6_addresses_lst = ipv6_addresses_lst

    def __eq__(self, others):
        if not isinstance(others, ListIPV6Interface):
            raise NotImplemented

        for ipv6 in self.ipv6_addresses_lst:
            if ipv6 not in others.ipv6_addresses_lst:
                return False

        for ipv6 in others.ipv6_addresses_lst:
            if ipv6 not in self.ipv6_addresses_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListIPV6Interface \n"
        for ipv6 in self.ipv6_addresses_lst:
            result = result + f"{ipv6}"
        return result + ">"
