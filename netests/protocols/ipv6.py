#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import ipaddress
from typing import List
from ipaddress import IPv6Address
from netests.constants import NOT_SET
from netests.protocols.ip import IPAddress


class IPV6(IPAddress):
    ip_address: ipaddress.IPv6Address = NOT_SET

    @classmethod
    def deserialize(
        cls,
        ip_address=NOT_SET,
        netmask=NOT_SET
    ) -> "IPV6":
        try:
            IPv6Address(ip_address)
            return {
                "ip_address": ip_address,
                "netmask": netmask
            }
        except Exception:
            return {
                "ip_address": IPv6Address(),
                "netmask": NOT_SET
            }


class IPV6Interface(IPV6):
    ipv6_addresses: List[IPV6]

    def to_json(self):
        ret = list()
        for i in self.ipv6_addresses:
            if i is not None:
                ret.append(i.to_json())
        return ret
