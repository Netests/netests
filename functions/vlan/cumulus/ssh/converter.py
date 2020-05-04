#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from functions.global_tools import is_valid_ipv4_address
from functions.vlan.cumulus.vlan_cumulus_filters import (
    _filter_vlan_values,
    _cumulus_vlan_members_converter
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    VLAN_DATA_HOST_KEY,
    VLAN_VRF_DETAIL_KEY,
    VLAN_VRF_LIST_KEY,
    VLAN_VRF_MEMBERS_KEY,
)
from protocols.vlan import (
    VLAN,
    ListVLAN
)
from protocols.ipv4 import (
    IPV4,
    ListIPV4,
    IPV4Interface,
)
from protocols.ipv6 import (
    IPV6Interface,
    ListIPV6Interface
)


def _cumulus_vlan_ssh_converter(
    hostname: str(),
    cmd_output: list,
    bond_lst: list,
    filters
) -> ListVLAN:

    vlans_lst = ListVLAN(
        vlans_lst=list()
    )

    vlan_members = dict()

    if VLAN_VRF_MEMBERS_KEY in cmd_output.keys():
        vlan_members = _cumulus_vlan_members_converter(
            bond_lst=bond_lst,
            cmd_output=cmd_output.get(VLAN_VRF_MEMBERS_KEY),
            filters=filters
        )

    if VLAN_VRF_DETAIL_KEY in cmd_output.keys() and VLAN_VRF_LIST_KEY in cmd_output.keys():
        for vlan in cmd_output.get(VLAN_VRF_DETAIL_KEY):
            if "vlan" in vlan and "-v" not in vlan:
                vrf_name = "default"
                for vrf in cmd_output.get(VLAN_VRF_LIST_KEY):
                    if vlan in vrf[1]:
                        vrf_name = vrf[0]

                ipv4_addresses_lst = ListIPV4(
                    ipv4_addresses_lst=list()
                )

                ipv6_addresses_lst = ListIPV6Interface(
                    ipv6_addresses_lst=list()
                )

                if "ip_address" in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").keys():
                    for ip_addr in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("ip_address").get("allentries"):
                        index_slash = str(ip_addr).find("/")
                        if is_valid_ipv4_address(str(ip_addr)[:index_slash]):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=str(
                                        ip_addr)[:index_slash],
                                    netmask=str(ip_addr)[index_slash+1:]
                                )
                            )
                        else:
                            ipv6_addresses_lst.ipv6_addresses_lst.append(
                                IPV6Interface(
                                    ip_address_with_mask=str(ip_addr)
                                )
                            )

                    i = 0
                    fhrp_ipv4 = "0.0.0.0"
                    fhrp_ipv6 = "0.0.0.0"

                    while f"{vlan}-v{i}" in cmd_output.get(VLAN_VRF_DETAIL_KEY).keys():
                        temp_ip = cmd_output.get(VLAN_VRF_DETAIL_KEY).get(
                            f"{vlan}-v{i}").get("iface_obj").get("ip_address").get("allentries")[0]
                        index_slash_fhrp = str(temp_ip).find("/")

                        if is_valid_ipv4_address(str(temp_ip)[:index_slash_fhrp]):
                            fhrp_ipv4 = str(temp_ip)[:index_slash_fhrp]
                        else:
                            fhrp_ipv6 = str(temp_ip)[:index_slash_fhrp]

                        i += 1

                vlans_lst.vlans_lst.append(
                    VLAN(
                        vlan_name=vlan,
                        vlan_id=str(vlan)[4:],
                        vlan_descr=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) if cmd_output.get(
                            VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) != "" else NOT_SET,
                        vrf_name=vrf_name,
                        ipv6_addresses=ipv6_addresses_lst,
                        fhrp_ipv6_address=fhrp_ipv6,
                        ipv4_addresses=ipv4_addresses_lst,
                        fhrp_ipv4_address=fhrp_ipv4,
                        ports_members=vlan_members.get(str(vlan)[4:], list()),
                        mac_address=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(
                            vlan).get("iface_obj").get("mac", NOT_SET)

                    )
                )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(vlans_lst)

    return vlans_lst
