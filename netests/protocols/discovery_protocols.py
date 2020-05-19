#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests.constants import NOT_SET


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

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port) or (
                self.local_name == other.neighbor_name and
                self.local_port == other.neighbor_port and
                self.neighbor_name == other.local_name and
                self.neighbor_port == other.local_port)

    def __repr__(self):
        return f"<{type(self)} local_name={self.local_name}\n" \
               f"local_port={self.local_port}\n" \
               f"neighbor_mgmt_ip={self.neighbor_mgmt_ip}\n" \
               f"neighbor_name={self.neighbor_name}\n" \
               f"neighbor_port={self.neighbor_port}\n" \
               f"neighbor_os={self.neighbor_os}\n" \
               f"neighbor_type={self.neighbor_type}>\n"

    def to_json(self):
        return {
            "local_name": self.local_name,
            "local_port": self.local_port,
            "neighbor_mgmt_ip": self.neighbor_mgmt_ip,
            "neighbor_name": self.neighbor_name,
            "neighbor_port": self.neighbor_port,
            "neighbor_os": self.neighbor_os,
            "neighbor_type": self.neighbor_type
        }
