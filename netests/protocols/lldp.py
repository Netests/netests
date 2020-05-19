#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.protocols.discovery_protocols import DiscoveryProtocols


ERROR_HEADER = "Error import [lldp.py]"


class LLDP(DiscoveryProtocols):

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
        super(LLDP, self).__init__(local_name,
                                   local_port,
                                   neighbor_name,
                                   neighbor_port,
                                   neighbor_os,
                                   neighbor_mgmt_ip,
                                   neighbor_type,
                                   options)

    def __eq__(self, other):
        if not isinstance(other, LLDP):
            return NotImplementedError()

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port)

    def __repr__(self):
        return super(LLDP, self).__repr__()

    def to_json(self):
        return super(LLDP, self).to_json()


class ListLLDP:

    lldp_neighbors_lst: list

    def __init__(self, lldp_neighbors_lst: list()):
        self.lldp_neighbors_lst = lldp_neighbors_lst

    def __eq__(self, others):
        if not isinstance(others, ListLLDP):
            raise NotImplementedError()

        for lldp in self.lldp_neighbors_lst:
            if lldp not in others.lldp_neighbors_lst:
                return False

        for lldp in others.lldp_neighbors_lst:
            if lldp not in self.lldp_neighbors_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListLLDP \n"
        for lldp in self.lldp_neighbors_lst:
            result = result + f"{lldp}"
        return result + ">"

    def to_json(self):
        data = list()
        for lldp in self.lldp_neighbors_lst:
            data.append(lldp.to_json())
        return data
