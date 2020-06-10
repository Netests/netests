#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests import log
from netests.constants import COMPARE_OPTION_KEY, PRINT_OPTION_KEY, NOT_SET


ERROR_HEADER = "Error import [discovery_protocols.py]"


class DiscoveryProtocols(ABC):

    local_name: str
    local_port: str
    neighbor_name: str
    neighbor_port: str
    neighbor_os: str
    neighbor_mgmt_ip: str
    neighbor_type: list
    options: dict

    def __init__(
        self,
        local_name=NOT_SET,
        local_port=NOT_SET,
        neighbor_name=NOT_SET,
        neighbor_port=NOT_SET,
        neighbor_os=NOT_SET,
        neighbor_mgmt_ip=NOT_SET,
        neighbor_type=list(),
        options={}
    ):
        self.local_name = local_name
        self.local_port = local_port
        self.neighbor_name = neighbor_name
        self.neighbor_port = neighbor_port
        self.neighbor_os = neighbor_os
        self.neighbor_mgmt_ip = neighbor_mgmt_ip
        self.neighbor_type = neighbor_type
        self.options = options

    def __eq__(self, other):
        if not isinstance(other, DiscoveryProtocols):
            return NotImplemented

        if COMPARE_OPTION_KEY in self.options.keys():
            log.debug(f"Compare modified function\noptions={self.options}")

            is_equal = True
            if self.options.get(COMPARE_OPTION_KEY).get('local_name', True):
                if str(self.local_name) != str(other.local_name):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('local_name', True):
                if str(self.local_name) != str(other.local_name):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('neighbor_name', True):
                if str(self.neighbor_name) != str(other.neighbor_name):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('neighbor_port', True):
                if str(self.neighbor_port) != str(other.neighbor_port):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('neighbor_mgmt_ip', False):
                if str(self.neighbor_mgmt_ip) != str(other.neighbor_mgmt_ip):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('neighbor_type', False):
                if str(self.neighbor_type) != str(other.neighbor_type):
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('neighbor_os', False):
                if str(self.neighbor_os) != str(other.neighbor_os):
                    is_equal = False

            log.debug(
                "Result for modified compare function\n"
                f"is_equal={is_equal}"
            )

            return is_equal
        else:
            log.debug(f"Compare standard function\noptions={self.options}")

            is_equal = (
                self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port
            )

            log.debug(
                "Result for standard compare function\n"
                f"is_equal={is_equal}"
            )

            return is_equal

    def __repr__(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = f"<{type(self)}\n"
            if self.options.get(PRINT_OPTION_KEY).get('local_name', True):
                ret += f"\t\tlocal_name={self.local_name}\n"
            if self.options.get(PRINT_OPTION_KEY).get('local_port', True):
                ret += f"\t\tlocal_port={self.local_port}\n"
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_name', True):
                ret += f"\t\tneighbor_name={self.neighbor_name}\n"
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_port', True):
                ret += f"\t\tneighbor_port={self.neighbor_port}\n"
            if self.options.get(PRINT_OPTION_KEY) \
                           .get('neighbor_mgmt_ip', True):
                ret += f"\t\tneighbor_mgmt_ip={self.neighbor_mgmt_ip}\n"
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_os', True):
                ret += f"\t\tneighbor_os={self.neighbor_os}\n"
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_type', True):
                ret += f"\t\tneighbor_type={self.neighbor_type}\n"
            return ret + ">\n"
        else:
            return f"<{type(self)}\n" \
                   f"\t\tlocal_name={self.local_name}\n" \
                   f"\t\tlocal_port={self.local_port}\n" \
                   f"\t\tneighbor_name={self.neighbor_name}\n" \
                   f"\t\tneighbor_port={self.neighbor_port}\n" \
                   f"\t\tneighbor_mgmt_ip={self.neighbor_mgmt_ip}\n" \
                   f"\t\tneighbor_os={self.neighbor_os}\n" \
                   f"\t\tneighbor_type={self.neighbor_type}\n" \
                   ">\n"

    def to_json(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = dict()
            if self.options.get(PRINT_OPTION_KEY).get('local_name', True):
                ret['local_name'] = self.local_name
            if self.options.get(PRINT_OPTION_KEY).get('local_port', True):
                ret['local_port'] = self.local_port
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_name', True):
                ret['neighbor_name'] = self.neighbor_name
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_port', True):
                ret['neighbor_port'] = self.neighbor_port
            if self.options.get(PRINT_OPTION_KEY) \
                           .get('neighbor_mgmt_ip', True):
                ret['neighbor_mgmt_ip'] = self.neighbor_mgmt_ip
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_os', True):
                ret['neighbor_os'] = self.neighbor_os
            if self.options.get(PRINT_OPTION_KEY).get('neighbor_type', True):
                ret['neighbor_type'] = self.neighbor_type
            return ret
        else:
            return {
                "local_name": self.local_name,
                "local_port": self.local_port,
                "neighbor_name": self.neighbor_name,
                "neighbor_port": self.neighbor_port,
                "neighbor_mgmt_ip": self.neighbor_mgmt_ip,
                "neighbor_os": self.neighbor_os,
                "neighbor_type": self.neighbor_type
            }
