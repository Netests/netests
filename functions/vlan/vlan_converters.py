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
    from protocols.ip import ListIPAddress, IPAddress
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ip")
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
            if "vlan" in vlan and "v0" not in vlan:
                vrf_name = "default"
                for vrf in cmd_output.get(VLAN_VRF_LIST_KEY):
                    if vlan in vrf[1]:
                        vrf_name = vrf[0]

                fhrp_ip = "0.0.0.0"
                ip_addresses_lst = ListIPAddress(
                    ip_addresses_lst=list()
                )

                if "ip_address" in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").keys():
                    for ip_addr in cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("ip_address").get("allentries"):
                        index_slash = str(ip_addr).find("/")
                        ip_addresses_lst.ip_addresses_lst.append(
                            IPAddress(
                                ip_address=str(ip_addr)[:index_slash],
                                netmask=str(ip_addr)[index_slash+1:]
                            )
                        )

                    if f"{vlan}-v0" in cmd_output.get(VLAN_VRF_DETAIL_KEY).keys():
                        temp_ip = cmd_output.get(VLAN_VRF_DETAIL_KEY).get(f"{vlan}-v0").get("iface_obj").get("ip_address").get("allentries")[0]
                        index_slash_fhrp = str(temp_ip).find("/")
                        fhrp_ip = str(temp_ip)[:index_slash_fhrp]

                vlans_lst.vlans_lst.append(
                    VLAN(
                        vlan_name=vlan,
                        vlan_id=str(vlan)[4:],
                        vlan_descr=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) if cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("description", NOT_SET) != "" else NOT_SET,
                        vrf_name=vrf_name,
                        ip_address=ip_addresses_lst,
                        fhrp_ip_address=fhrp_ip,
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
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper vlan converter
#
def _juniper_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

