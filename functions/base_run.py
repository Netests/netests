#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core import Nornir
from functions.bgp.bgp_gets import get_bgp
from functions.bgp.bgp_compare import compare_bgp
from functions.bgp.bgp_checks import get_bgp_up
from functions.bond.bond_get import get_bond
from functions.bond.bond_compare import compare_bond
from functions.discovery_protocols.cdp.cdp_get import get_cdp
from functions.discovery_protocols.cdp.cdp_compare import compare_cdp
from functions.discovery_protocols.lldp.lldp_get import get_lldp
from functions.discovery_protocols.lldp.lldp_compare import compare_lldp
from functions.infos.infos_get import get_infos
from functions.infos.infos_compare import compare_infos
from functions.ip.ipv4.ipv4_get import get_ipv4
from functions.ip.ipv4.ipv4_compare import compare_ipv4
from functions.ip.ipv6.ipv6_get import get_ipv6
from functions.ip.ipv6.ipv6_compare import compare_ipv6
from functions.l2vni.l2vni_get import get_l2vni
from functions.l2vni.l2vni_compare import compare_l2vni
from functions.mlag.mlag_get import get_mlag
from functions.mlag.mlag_compare import compare_mlag
from functions.mtu.mtu_get import get_mtu
from functions.mtu.mtu_compare import compare_mtu
from functions.ospf.ospf_get import get_ospf
from functions.ospf.ospf_compare import compare_ospf
from functions.ping.ping_execute import execute_ping
from functions.socket.socket_execute import execute_socket
from functions.static.static_get import get_static
from functions.static.static_compare import compare_static
from functions.vlan.vlan_get import get_vlan
from functions.vlan.vlan_compare import compare_vlan
from functions.vrf.vrf_get import get_vrf
from functions.vrf.vrf_compare import compare_vrf
from const.constants import (
    BGP_SRC_FILENAME,
    BOND_SRC_FILENAME,
    CDP_SRC_FILENAME,
    LLDP_SRC_FILENAME,
    INFOS_SRC_FILENAME,
    IPV4_SRC_FILENAME,
    IPV6_SRC_FILENAME,
    L2VNI_SRC_FILENAME,
    MLAG_SRC_FILENAME,
    MTU_SRC_FILENAME,
    OSPF_SRC_FILENAME,
    PING_SRC_FILENAME,
    SOCKET_SRC_FILENAME,
    STATIC_SRC_FILENAME,
    VLAN_SRC_FILENAME,
    VRF_SRC_FILENAME,
    PATH_TO_VERITY_FILES
)

HEADER = "[netests - base_run.py]"
RUN = {
    "bgp": {
        "function": get_bgp,
        "file": BGP_SRC_FILENAME,
        "compare": compare_bgp
    },
    "bgp_all_up": {
        "function": get_bgp_up,
        "file": BGP_SRC_FILENAME
    },
    "bond": {
        "function": get_bond,
        "file": BOND_SRC_FILENAME,
        "compare": compare_bond
    },
    "cdp": {
        "function": get_cdp,
        "file": CDP_SRC_FILENAME,
        "compare": compare_cdp
    },
    "lldp": {
        "function": get_lldp,
        "file": LLDP_SRC_FILENAME,
        "compare": compare_lldp
    },
    "infos": {
        "function": get_infos,
        "file": INFOS_SRC_FILENAME,
        "compare": compare_infos
    },
    "ipv4": {
        "function": get_ipv4,
        "file": IPV4_SRC_FILENAME,
        "compare": compare_ipv4
    },
    "ipv6": {
        "function": get_ipv6,
        "file": IPV6_SRC_FILENAME,
        "compare": compare_ipv6
    },
    "l2vni": {
        "function": get_l2vni,
        "file": L2VNI_SRC_FILENAME,
        "compare": compare_l2vni
    },
    "mlag": {
        "function": get_mlag,
        "file": MLAG_SRC_FILENAME,
        "compare": compare_mlag
    },
    "mtu": {
        "function": get_mtu,
        "file": MTU_SRC_FILENAME,
        "compare": compare_mtu
    },
    "ospf": {
        "function": get_ospf,
        "file": OSPF_SRC_FILENAME,
        "compare": compare_ospf
    },
    "ping": {
        "function": execute_ping,
        "file": PING_SRC_FILENAME
    },
    "socket": {
        "function": execute_socket,
        "file": SOCKET_SRC_FILENAME
    },
    "static": {
        "function": get_static,
        "file": STATIC_SRC_FILENAME,
        "compare": compare_static
    },
    "vlan": {
        "function": get_vlan,
        "file": VLAN_SRC_FILENAME,
        "compare": compare_vlan
    },
    "vrf": {
        "function": get_vrf,
        "file": VRF_SRC_FILENAME,
        "compare": compare_vrf
    }
}


def run_base(nr: Nornir, protocol: str, parameters: dict) -> bool:
    if (
        parameters.get('test', False) is True or
        str(parameters.get('test', False)).upper() == "INFO"
    ):
        same = RUN.get(protocol).get('function')(
            nr=nr,
            filters=parameters.get('filters'),
            level=parameters.get('compare'),
            own_vars=parameters.get('own_vars')
        )
        if (
            protocol != "ping" and
            protocol != "socket" and
            protocol != "bgp_all_up"
        ):  
            same = RUN.get(protocol).get('compare')(
                nr=nr,
                own_vars=parameters.get('own_vars')
            )

        print(
            f"{HEADER} ({protocol}) defined in {PATH_TO_VERITY_FILES}"
            f"{RUN.get(protocol).get('file')} work = {same} !!"
        )

        return (
            parameters.get('test', False) is True and
            same is False
        )

    else:
        return True
