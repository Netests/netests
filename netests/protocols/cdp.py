#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.protocols.discovery_protocols import DiscoveryProtocols


class CDP(DiscoveryProtocols):

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
        super(CDP, self).__init__(local_name,
                                  local_port,
                                  neighbor_name,
                                  neighbor_port,
                                  neighbor_os,
                                  neighbor_mgmt_ip,
                                  neighbor_type,
                                  options)

    def __eq__(self, other):
        if not isinstance(other, CDP):
            return NotImplementedError()

        return (self.local_name == other.local_name and
                self.local_port == other.local_port and
                self.neighbor_name == other.neighbor_name and
                self.neighbor_port == other.neighbor_port)

    def __repr__(self):
        return super(CDP, self).__repr__()

    def to_json(self):
        return super(CDP, self).to_json()


class ListCDP:

    cdp_neighbors_lst: list

    def __init__(self, cdp_neighbors_lst: list()):
        self.cdp_neighbors_lst = cdp_neighbors_lst

    def __eq__(self, others):
        if not isinstance(others, ListCDP):
            raise NotImplementedError()

        for cdp in self.cdp_neighbors_lst:
            if cdp not in others.cdp_neighbors_lst:
                return False

        for cdp in others.cdp_neighbors_lst:
            if cdp not in self.cdp_neighbors_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListCDP \n"
        for cdp in self.cdp_neighbors_lst:
            result = result + f"{cdp}"
        return result + ">"

    def to_json(self):
        data = list()
        for cdp in self.cdp_neighbors_lst:
            data.append(cdp.to_json())
        return data
