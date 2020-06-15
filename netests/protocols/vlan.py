#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from typing import List, Optional
from netests.protocols.ipv4 import IPV4Interface
from netests.protocols.ipv6 import IPV6Interface
from netests.protocols._protocols import NetestsProtocol
from netests.constants import COMPARE_OPTION_KEY, PRINT_OPTION_KEY, NOT_SET


class VLAN(NetestsProtocol):
    id: Optional[int] = NOT_SET
    name: Optional[str] = NOT_SET
    vrf_name: Optional[str] = NOT_SET
    ipv4_addresses: Optional[IPV4Interface] = None
    ipv6_addresses: Optional[IPV6Interface] = None
    assigned_ports: Optional[List[str]] = list()

    def __eq__(self, other):
        if not isinstance(other, VLAN):
            raise NotImplementedError()

        if COMPARE_OPTION_KEY in self.options.keys():
            log.debug(f"Compare modified function\noptions={self.options}")
            is_equal = True
            if self.options.get(PRINT_OPTION_KEY).get('id', True):
                if self.id != other.id:
                    is_equal = False
            if self.options.get(PRINT_OPTION_KEY).get('name', True):
                if self.name != other.name:
                    is_equal = False
            if self.options.get(PRINT_OPTION_KEY).get('vrf_name', True):
                if self.vrf_name != other.vrf_name:
                    is_equal = False
            if self.options.get(PRINT_OPTION_KEY).get('ipv4_addresses', True):
                if self.ipv4_addresses != other.ipv4_addresses:
                    is_equal = False
            if self.options.get(PRINT_OPTION_KEY).get('ipv6_addresses', True):
                if self.ipv6_addresses != other.ipv6_addresses:
                    is_equal = False
            if self.options.get(PRINT_OPTION_KEY).get('assigned_ports', True):
                if self.assigned_ports != other.assigned_ports:
                    is_equal = False
            return is_equal
        else:
            return (
                self.name == other.name and
                self.id == other.id
            )

    def to_json(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = dict()
            if self.options.get(PRINT_OPTION_KEY).get('id', True):
                ret['id'] = self.id
            if self.options.get(PRINT_OPTION_KEY).get('name', True):
                ret['name'] = self.name
            if self.options.get(PRINT_OPTION_KEY).get('vrf_name', True):
                ret['vrf_name'] = self.vrf_name
            if self.options.get(PRINT_OPTION_KEY).get('ipv4_addresses', True):
                ret['ipv4_addresses'] = self.ipv4_addresses
            if self.options.get(PRINT_OPTION_KEY).get('ipv6_addresses', True):
                ret['ipv6_addresses'] = self.ipv6_addresses
            if self.options.get(PRINT_OPTION_KEY).get('assigned_ports', True):
                ret['assigned_ports'] = self.assigned_ports
            return ret
        else:
            return {
                "id": self.id,
                "name": self.name,
                "vrf_name": self.vrf_name,
                "ipv4_addresses": self.ipv4_addresses.to_json(),
                "ipv6_addresses": self.ipv6_addresses.to_json(),
                "assigned_ports": self.assigned_ports
            }


class ListVLAN(NetestsProtocol):
    vlan_lst: List[VLAN] = list()

    def to_json(self):
        ret = list()
        for i in self.vlan_lst:
            if i is not None:
                ret.append(i.to_json())
        return ret
