#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from typing import List, Optional
from netests.protocols._protocols import NetestsProtocol
from netests.constants import COMPARE_OPTION_KEY, PRINT_OPTION_KEY, NOT_SET


class ISISAdjacency(NetestsProtocol):
    session_state: str = NOT_SET
    level_type: str = NOT_SET
    circuit_type: Optional[str] = NOT_SET
    local_interface_name: Optional[str] = NOT_SET
    neighbor_sys_name: Optional[str] = NOT_SET
    neighbor_ip_addr: Optional[str] = NOT_SET
    snap: Optional[str] = NOT_SET

    def __eq__(self, other):
        if not isinstance(other, ISISAdjacency):
            raise NotImplementedError()

        if COMPARE_OPTION_KEY in self.options.keys():
            log.debug(f"Compare modified function\noptions={self.options}")
            is_equal = True
            if self.options.get(COMPARE_OPTION_KEY).get('session_state', True):
                if self.session_state != other.session_state:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('level_type', True):
                if self.level_type != other.level_type:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY).get('circuit_type', True):
                if self.circuit_type != other.circuit_type:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('local_interface_name', True):
                if self.local_interface_name != other.local_interface_name:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('neighbor_sys_name', True):
                if self.neighbor_sys_name != other.neighbor_sys_name:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('neighbor_ip_addr', True):
                if self.neighbor_ip_addr != other.neighbor_ip_addr:
                    is_equal = False
            if self.options.get(COMPARE_OPTION_KEY) \
                           .get('snap', True):
                if self.snap != other.snap:
                    is_equal = False
            return is_equal
        else:
            return (
                self.session_state == other.session_state and
                self.level_type == other.level_type and
                self.neighbor_sys_name == other.neighbor_sys_name
            )

    def to_json(self):
        if PRINT_OPTION_KEY in self.options.keys():
            ret = dict()
            if self.options.get(PRINT_OPTION_KEY).get('session_state', True):
                ret['session_state'] = self.session_state
            if self.options.get(PRINT_OPTION_KEY).get('level_type', True):
                ret['level_type'] = self.level_type
            if self.options.get(PRINT_OPTION_KEY).get('circuit_type', True):
                ret['circuit_type'] = self.circuit_type
            if self.options.get(PRINT_OPTION_KEY) \
                           .get('local_interface_name', True):
                ret['local_interface_name'] = self.local_interface_name
            if self.options.get(PRINT_OPTION_KEY) \
                           .get('neighbor_sys_name', True):
                ret['neighbor_sys_name'] = self.neighbor_sys_name
            if self.options.get(PRINT_OPTION_KEY) \
                           .get('neighbor_ip_addr', True):
                ret['neighbor_ip_addr'] = self.neighbor_ip_addr
            if self.options.get(PRINT_OPTION_KEY).get('snap', True):
                ret['snap'] = self.snap
            return ret
        else:
            return {
                "session_state": self.session_state,
                "level_type": self.level_type,
                "circuit_type": self.circuit_type,
                "local_interface_name": self.local_interface_name,
                "neighbor_sys_name": self.neighbor_sys_name,
                "neighbor_ip_addr": self.neighbor_ip_addr,
                "snap": self.snap
            }


class ListISISAdjacency(NetestsProtocol):
    isis_adj_lst: Optional[List[ISISAdjacency]] = list()

    def __eq__(self, others):
        if not isinstance(others, ListISISAdjacency):
            raise NotImplementedError()

        for isis_adj in self.isis_adj_lst:
            if isis_adj not in others.isis_adj_lst:
                return False

        for isis_adj in others.isis_adj_lst:
            if isis_adj not in self.isis_adj_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListISISAdjacency \n"
        for isis_adj in self.isis_adj_lst:
            result = result + f"{isis_adj}"
        return result + ">"

    def to_json(self):
        ret = list()
        for i in self.isis_adj_lst:
            if i is not None:
                ret.append(i.to_json())
        return ret


class ISISAdjacencyVRF(NetestsProtocol):
    router_id: str = NOT_SET
    system_id: str = NOT_SET
    area_id: str = NOT_SET
    vrf_name: str = NOT_SET
    isis_adj_lst: ListISISAdjacency = list()

    def to_json(self):
        return {
            'router_id': self.router_id,
            'system_id': self.system_id,
            'area_id': self.area_id,
            'isis_adj_lst': self.isis_adj_lst.to_json(),
        }


class ListISISAdjacencyVRF(NetestsProtocol):
    isis_vrf_lst: List[ISISAdjacencyVRF] = list()


class ISIS(NetestsProtocol):
    hostname: str = NOT_SET
    isis_vrf_lst: ListISISAdjacencyVRF = list()
