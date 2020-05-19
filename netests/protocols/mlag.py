#/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET


class MLAG:

    hostname: str
    local_id: str
    peer_id: str
    peer_alive: str
    peer_int: str
    peer_ip: str
    sys_mac: str
    local_role: str
    peer_role: str
    local_priority: str
    peer_priority: str
    vxlan_anycast_ip: str

    def __init__(
        self,
        hostname=NOT_SET,
        local_id=NOT_SET,
        peer_id=NOT_SET,
        local_role=NOT_SET,
        peer_role=NOT_SET,
        peer_alive=NOT_SET,
        peer_int=NOT_SET,
        peer_ip=NOT_SET,
        sys_mac=NOT_SET,
        local_priority=NOT_SET,
        peer_priority=NOT_SET,
        vxlan_anycast_ip=NOT_SET
    ):
        self.hostname = hostname
        self.local_id = local_id
        self.peer_id = peer_id
        self.local_role = local_role
        self.peer_role = peer_role
        self.peer_alive = peer_alive
        self.peer_int = peer_int
        self.peer_ip = peer_ip
        self.sys_mac = sys_mac
        self.local_priority = local_priority
        self.peer_priority = peer_priority
        self.vxlan_anycast_ip = vxlan_anycast_ip

    def __eq__(self, other):
        if not isinstance(other, MLAG):
            return NotImplemented
        if (str(self.hostname) == str(self.hostname) and
                str(self.local_id) == str(other.local_id) and
                str(self.peer_id) == str(other.peer_id) and
                str(self.peer_int) == str(other.peer_int) and
                str(self.peer_ip) == str(other.peer_ip) and
                str(self.sys_mac) == str(other.sys_mac) and
                str(self.peer_alive) == str(other.peer_alive)):
            return True

    def __repr__(self):
        return f"<MLAG hostname={self.hostname} " \
               f"local_id={self.local_id} " \
               f"peer_id={self.peer_id} " \
               f"peer_int={self.peer_int} " \
               f"peer_ip={self.peer_ip} " \
               f"local_role={self.local_role} " \
               f"peer_role={self.peer_role} " \
               f"local_priority={self.local_priority} " \
               f"peer_priority={self.peer_priority} " \
               f"sys_mac={self.sys_mac} " \
               f"vxlan_anycast_ip={self.vxlan_anycast_ip} " \
               f"peer_alive={self.peer_alive}>\n"
