#/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET


class L2VNI:

    vxlan_int: str
    vtep_ip: str
    vni: str
    vrf: str
    multicast_gr_ip: str
    remote_vteps: list

    def __init__(
        self,
        vxlan_int=NOT_SET,
        vtep_ip="0.0.0.0",
        vni=NOT_SET,
        vrf=NOT_SET,
        remote_vteps=NOT_SET,
        multicast_gr_ip="0.0.0.0"
    ):
        self.vxlan_int = vxlan_int
        self.vtep_ip = vtep_ip
        self.vni = vni
        self.vrf = vrf
        self.remote_vteps = remote_vteps
        self.multicast_gr_ip = multicast_gr_ip

    def __eq__(self, other):
        if not isinstance(other, L2VNI):
            return NotImplemented

        if (str(self.vxlan_int) == str(self.vxlan_int) and
                str(self.vtep_ip) == str(other.vtep_ip) and
                str(self.vni) == str(other.vni) and
                str(self.vrf) == str(other.vrf) and
                str(self.multicast_gr_ip) == str(other.multicast_gr_ip)):
            return True

    def __repr__(self):
        return f"<L2VNI vxlan_int={self.vxlan_int} " \
               f"vtep_ip={self.vtep_ip} " \
               f"vni={self.vni} " \
               f"vrf={self.vrf} " \
               f"multicast_gr_ip={self.multicast_gr_ip} " \
               f"remote_vteps={self.remote_vteps}>\n"


class ListL2VNI:

    l2vni_lst: list

    def __init__(self, l2vni_lst: list()):
        self.l2vni_lst = l2vni_lst

    def __eq__(self, others):
        if not isinstance(others, ListL2VNI):
            raise NotImplemented

        for l2vni in self.l2vni_lst:
            if l2vni not in others.l2vni_lst:
                return False

        for l2vni in others.l2vni_lst:
            if l2vni not in self.l2vni_lst:
                return False

        return True

    def __repr__(self):
        result = "<ListL2VNI \n"
        for l2vni in self.l2vni_lst:
            result = result + f"{l2vni}"
        return result + ">"