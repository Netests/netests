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
ERROR_HEADER = "Error import [ipv6_converters.py]"
HEADER_GET = "[netests - ipv6_converters]"

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
    from protocols.ipv6 import IPV6, ListIPV6
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ipv6")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.global_tools import _generic_interface_filter
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

try:
    import ipaddress
except ImportError as importError:
    print(f"{ERROR_HEADER} ipaddress")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM ipv6 addresses converter
#
def _napalm_ipv6_converter(hostname:str(), plateform:str(), cmd_output:json, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus ipv6 addresses converter
#
def _cumulus_ipv6_converter(hostname:str(), plateform:str(), cmd_output:json, *, filters=dict()) -> ListIPV6:

    ipv6_addresses_lst = ListIPV6(
        hostname=hostname,
        ipv6_addresses_lst=list()
    )

    for interface_name, facts in cmd_output.items():
        # v0 = vrrp / vrr / hsrp / HA ip address
        # bridge is a Linux bridge
        if _generic_interface_filter(
                plateform=plateform,
                interface_name=_mapping_interface_name(
                    interface_name
                ),
                filters=filters
        ):

            for ip_address_in_interface in facts.get("iface_obj").get('ip_address').get('allentries'):
                if str(ip_address_in_interface).find("/") != -1:
                    index_slash = str(ip_address_in_interface).find("/")

                    try:
                        ipaddress.IPv6Address(ip_address_in_interface[:index_slash])
                        is_valid = True
                    except ipaddress.AddressValueError as e:
                        is_valid = False

                    if is_valid:
                        if "::1/128" not in ip_address_in_interface:

                            ipv6_addresses_lst.ipv6_addresses_lst.append(
                                IPV6(
                                    interface_name=_mapping_interface_name(
                                        interface_name
                                    ),
                                    ip_address_with_mask=ip_address_in_interface
                                )
                            )

    print(ipv6_addresses_lst)
    return ipv6_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus ipv6 addresses Converter
#
def _nexus_ipv6_converter(hostname:str(), plateform:str(), cmd_outputs:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS ipv6 addresses Converter
#
def _ios_ipv6_converter(hostname:str(), plateform:str(), cmd_output:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS XR ipv6 addresses Converter
#
def _iosxr_ipv6_converter(hostname:str(), plateform:str(), cmd_output:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista ipv6 addresses Converter
#
def _arista_ipv6_converter(hostname:str(), plateform:str(), cmd_output:json, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper ipv6 addresses Converter
#
def _juniper_ipv6_converter(hostname:str(), plateform:str(), cmd_output:dict, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP ipv6 addresses Converter
#
def _extreme_vsp_ipv6_converter(hostname: str(), plateform:str(), cmd_output: dict, *, get_vlan=True, get_loopback=True,
                                get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV6:
    pass