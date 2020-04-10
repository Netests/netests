#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
from functions.discovery_protocols.discovery_functions import (
    _mapping_interface_name
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    VLAN_GET_L2,
    VLAN_GET_L3,
    VLAN_GET_INT
)
from protocols.vlan import (
    VLAN,
    ListVLAN,
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

def _arista_vlan_ssh_converter(
    cmd_output={},
    filters={},
    level=None,
    own_vars={}
) -> ListVLAN:

    if cmd_output is None:
        return None

    vlans_lst = ListVLAN(
        vlans_lst=list()
    )

    if "vlans" in cmd_output.get(VLAN_GET_L2).keys():
        for vlan in cmd_output.get(VLAN_GET_L2).get("vlans"):

            ports_members = list()
            for port in cmd_output.get(VLAN_GET_L2).get("vlans").get(vlan).get("interfaces"):
                if "Cpu" not in port:
                    ports_members.append(
                        _mapping_interface_name(
                            port
                        )
                    )

            vrf_name = NOT_SET
            if "interfaces" in cmd_output.get(VLAN_GET_L3).keys():
                if f"Vlan{vlan}" in cmd_output.get(VLAN_GET_L3).get("interfaces").keys():
                    vrf_name = cmd_output.get(VLAN_GET_L3).get(
                        "interfaces").get(f"Vlan{vlan}").get("vrf", NOT_SET)

            mac_address = NOT_SET
            if "interfaces" in cmd_output.get(VLAN_GET_INT).keys():
                if f"Vlan{vlan}" in cmd_output.get(VLAN_GET_INT).get("interfaces").keys():
                    mac_address = cmd_output.get(VLAN_GET_INT).get(
                        "interfaces").get(f"Vlan{vlan}").get("physicalAddress")

            ipv4_addresses_lst = ListIPV4(
                ipv4_addresses_lst=list()
            )

            ipv6_addresses_lst = ListIPV6Interface(
                ipv6_addresses_lst=list()
            )

            if "interfaces" in cmd_output.get(VLAN_GET_L3).keys():
                if f"Vlan{vlan}" in cmd_output.get(VLAN_GET_L3).get("interfaces"):
                    if "interfaceAddress" in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").keys():
                        for secondary_ip in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("secondaryIpsOrderedList"):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=secondary_ip.get(
                                        "address"),
                                    netmask=secondary_ip.get("maskLen"),
                                )
                            )

                        if "address" in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("primaryIp"):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=cmd_output.get(VLAN_GET_L3).get("interfaces").get(
                                        f"Vlan{vlan}").get("interfaceAddress").get("primaryIp").get("address"),
                                    netmask=cmd_output.get(VLAN_GET_L3).get("interfaces").get(
                                        f"Vlan{vlan}").get("interfaceAddress").get("primaryIp").get("maskLen"),
                                )
                            )

                    if "interfaceAddressIp6" in cmd_output.get(VLAN_GET_INT).get("interfaces").get(f"Vlan{vlan}").keys():
                        for ipv6_addr in cmd_output.get(VLAN_GET_INT).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddressIp6").get("globalUnicastIp6s"):

                           index_slash = str(ipv6_addr.get("subnet")).find("/")

                           ipv6_addresses_lst.ipv6_addresses_lst.append(
                               IPV6Interface(
                                   ip_address_with_mask=ipv6_addr.get(
                                       "address"),
                                   netmask=str(ipv6_addr.get("subnet"))[
                                       index_slash+1:]
                               )
                           )

            vlans_lst.vlans_lst.append(
                VLAN(
                    vlan_name=cmd_output.get(VLAN_GET_L2).get("vlans").get(vlan).get("name", NOT_SET),
                    vlan_id=vlan,
                    vlan_descr=NOT_SET,
                    vrf_name=vrf_name,
                    ipv6_addresses=ipv6_addresses_lst,
                    fhrp_ipv6_address="0.0.0.0",
                    ipv4_addresses=ipv4_addresses_lst,
                    fhrp_ipv4_address="0.0.0.0",
                    ports_members=ports_members,
                    mac_address=mac_address

                )
            )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(vlans_lst)

    return vlans_lst
