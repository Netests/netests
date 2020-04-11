#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import *
from protocols.vlan import VLAN, ListVLAN
from protocols.ipv4 import IPV4, ListIPV4
from protocols.ipv6 import IPV6, ListIPV6, IPV6Interface, ListIPV6Interface
from functions.global_tools import is_valid_ipv4_address
from functions.discovery_protocols.discovery_functions import _mapping_interface_name
import json


def _filter_vlan_values(bond_lst:list, result_dict:dict, interface_name, vlan_id, filters:dict) -> dict:
    """
    This function will apply filters defined in netests configurations file.
    vlan:
      test: true
      filters:
        get_default: false
        get_bridge: false
        get_vni: false

    :param result_dict:
    :param interface_name:
    :param vlan_id:
    :return restult_dict:
    """

    if str(vlan_id) not in result_dict.keys():
        if str(vlan_id) == "1" and filters.get("get_default", True) is True or \
                str(vlan_id) != "1":
            result_dict[str(vlan_id)] = list()

    if str(vlan_id) in result_dict.keys():
        if ('bridge' in str(interface_name) and filters.get("get_bridge", True) is True) or \
                (str(interface_name) in bond_lst and filters.get("get_lag", True) is True) or \
                ('vni' in str(interface_name) and filters.get("get_vni", True) is True) or \
                ("bridge" not in str(interface_name) and "vni" not in str(interface_name) and \
                 "peerlink" not in str(interface_name) and str(interface_name) not in bond_lst):

            if ('peerlink' in str(interface_name) and filters.get("get_peerlink", True) is True) or \
                    "peerlink" not in str(interface_name):

                result_dict.get(str(vlan_id)).append(str(interface_name))

    return result_dict

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM vlan converter
#
def _napalm_vlan_converter(bond_lst:list, cmd_output:json) -> ListVLAN:
    pass


# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus vlan converter
#
def _cumulus_vlan_converter(bond_lst:list, cmd_output:json, filters:dict) -> ListVLAN:

    if cmd_output is None:
        return None

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
                                    ip_address_with_mask=str(ip_addr)[:index_slash],
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
                        ports_members=vlan_members.get(str(vlan)[4:], list()),
                        mac_address=cmd_output.get(VLAN_VRF_DETAIL_KEY).get(vlan).get("iface_obj").get("mac", NOT_SET)

                    )
                )

    return vlans_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus VLAN members converter
#
def _cumulus_vlan_members_converter(bond_lst:list, cmd_output:json, filters:dict) -> json:
    """
    On Cumulus devices with the command "net show bridge vlan json" you get the interface vlan members.
    Example :
        swp1 -> vlan100, vlan101, etc.
        swp2 -> vlan200, vlan101, etc
        vni100 -> vlan100

    This function will convert this output to have vlan interfaces members.
    Example :
        vlan100 -> swp1, vni100
        vlan101 -> swp1, swp2
        vlan200 -> swp2

    :param cmd_output:
    :return json:
    """

    if cmd_output is None:
        return None

    result_dict = dict()

    for interface_name in cmd_output:
        for vlan in cmd_output.get(interface_name):

            if "vlanEnd" in vlan.keys():
                i = 0
                while vlan.get("vlan") + i <=  vlan.get("vlanEnd"):
                    result_dict = _filter_vlan_values(
                        bond_lst=bond_lst,
                        result_dict=result_dict,
                        interface_name=interface_name,
                        vlan_id=str(vlan.get("vlan")+i),
                        filters=filters
                    )
                    i += 1

            else:
                result_dict = _filter_vlan_values(
                    bond_lst=bond_lst,
                    result_dict=result_dict,
                    interface_name=interface_name,
                    vlan_id=str(vlan.get("vlan")),
                    filters=filters
                )

    return result_dict

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
# Juniper vlan converter
#
def _juniper_vlan_converter(hostname:str(), cmd_output:json) -> ListVLAN:
    pass

