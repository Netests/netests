#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [vlan_converters.py]"
HEADER_GET = "[netests - vlan_converters]"

########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.vlan import VLAN, ListVLAN
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vlan")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.ipv4 import IPV4, ListIPV4
    from protocols.ipv6 import IPV6, ListIPV6
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ip")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.global_tools import is_valid_ipv4_address
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM vlan converter
#
def _napalm_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus vlan converter
#
def _cumulus_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:

    if cmd_output is None:
        return None

    vlans_lst = ListVLAN(
        vlans_lst=list()
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

                ipv6_addresses_lst = ListIPV6(
                    ipv6_addresses_lst=list()
                )

                if "ip_address" in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").keys():
                    for ip_addr in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("ip_address").get("allentries"):
                        index_slash = str(ip_addr).find("/")
                        if is_valid_ipv4_address(str(ip_addr)[:index_slash]):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=str(ip_addr)[:index_slash],
                                    netmask=str(ip_addr)[index_slash+1:]
                                )
                            )
                        else:
                            ipv6_addresses_lst.ipv6_addresses_lst.append(
                                IPV6(
                                    ip_address_with_mask=str(ip_addr)
                                )
                            )

                    i = 0
                    fhrp_ipv4 = "0.0.0.0"
                    fhrp_ipv6 = "0.0.0.0"

                    while f"{vlan}-v{i}" in cmd_output.get(VLAN_VRF_DETAIL_KEY).keys():
                        temp_ip = cmd_output.get(VLAN_VRF_DETAIL_KEY).get(f"{vlan}-v{i}").get("iface_obj").get("ip_address").get("allentries")[0]
                        index_slash_fhrp = str(temp_ip).find("/")

                        if is_valid_ipv4_address(str(temp_ip)[:index_slash_fhrp]):
                            fhrp_ipv4 = str(temp_ip)[:index_slash_fhrp]
                        else:
                            fhrp_ipv6 = str(temp_ip)[:index_slash_fhrp]

                        i+=1

                vlans_lst.vlans_lst.append(
                    VLAN(
                        vlan_name=vlan,
                        vlan_id=str(vlan)[4:],
                        vlan_descr=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) if cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) != "" else NOT_SET,
                        vrf_name=vrf_name,
                        ipv6_addresses=ipv6_addresses_lst,
                        fhrp_ipv6_address=fhrp_ipv6,
                        ipv4_addresses=ipv4_addresses_lst,
                        fhrp_ipv4_address=fhrp_ipv4,
                        ports_members=list(),
                        mac_address=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("mac", NOT_SET)

                    )
                )

    return vlans_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme VSP vlan converter
#
def _extreme_vsp_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS vlan converter
#
def _ios_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus vlan converter
#
def _nexus_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista vlan converter
#
def _arista_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:

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
                    vrf_name = cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("vrf", NOT_SET)

            mac_address = NOT_SET
            if "interfaces" in cmd_output.get(VLAN_GET_INT).keys():
                if f"Vlan{vlan}" in cmd_output.get(VLAN_GET_INT).get("interfaces").keys():
                    mac_address = cmd_output.get(VLAN_GET_INT).get("interfaces").get(f"Vlan{vlan}").get("physicalAddress")


            ipv4_addresses_lst = ListIPV4(
                ipv4_addresses_lst=list()
            )

            ipv6_addresses_lst = ListIPV6(
                ipv6_addresses_lst=list()
            )

            if "interfaces" in cmd_output.get(VLAN_GET_L3).keys():
                if f"Vlan{vlan}" in cmd_output.get(VLAN_GET_L3).get("interfaces"):
                    if "interfaceAddress" in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").keys():
                        for secondary_ip in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("secondaryIpsOrderedList"):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=secondary_ip.get("address"),
                                    netmask=secondary_ip.get("maskLen"),
                                )
                            )

                        if "address" in cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("primaryIp"):
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    ip_address_with_mask=cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("primaryIp").get("address"),
                                    netmask=cmd_output.get(VLAN_GET_L3).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddress").get("primaryIp").get("maskLen"),
                                )
                            )

                    if "interfaceAddressIp6" in cmd_output.get(VLAN_GET_INT).get("interfaces").get(f"Vlan{vlan}").keys():
                        for ipv6_addr in cmd_output.get(VLAN_GET_INT).get("interfaces").get(f"Vlan{vlan}").get("interfaceAddressIp6").get("globalUnicastIp6s"):

                           index_slash = str(ipv6_addr.get("subnet")).find("/")

                           ipv6_addresses_lst.ipv6_addresses_lst.append(
                               IPV6(
                                   ip_address_with_mask=ipv6_addr.get("address"),
                                   netmask=str(ipv6_addr.get("subnet"))[index_slash+1:]
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

    return vlans_lst


# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper vlan converter
#
def _juniper_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

