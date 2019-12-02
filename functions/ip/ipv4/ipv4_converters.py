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
ERROR_HEADER = "Error import [ipv4_converters.py]"
HEADER_GET = "[netests - ipv4_converters]"

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
    from protocols.ipv4 import IPV4, ListIPV4
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ipv4")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
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
# NAPALM IPv4 addresses converter
#
def _napalm_ipv4_converter(hostname:str(), cmd_output:json) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface_name in cmd_output.get('get_interfaces_ip'):

        for ip_addr in cmd_output.get('get_interfaces_ip').get(interface_name).get('ipv4'):

            ipv4_addresses_lst.ipv4_addresses_lst.append(
                IPV4(
                    interface_name=_mapping_interface_name(
                        interface_name
                    ),
                    ip_address_with_mask=ip_addr,
                    netmask=cmd_output.get('get_interfaces_ip').get(interface_name).get('ipv4').get(ip_addr).get('prefix_length')
                )
            )

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus IPv4 addresses converter
#
def _cumulus_ipv4_converter(hostname:str(), cmd_output:json) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface_name, facts in cmd_output.items():

        # v0 = vrrp / vrr / hsrp / HA ip address
        # bridge is a Linux bridge
        if "bridge" not in interface_name or "v0" not in interface_name:

            for ip_address_in_interface in facts.get("iface_obj").get('ip_address').get('allentries'):

                if "/128" not in ip_address_in_interface and "/64" not in ip_address_in_interface and \
                        "/48" not in ip_address_in_interface and "::" not in ip_address_in_interface and \
                        "127.0.0.1" not in ip_address_in_interface and "::1/128" not in ip_address_in_interface:

                    ipv4_obj = IPV4(
                        interface_name=_mapping_interface_name(interface_name),
                        ip_address_with_mask=ip_address_in_interface
                    )

                    ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

    print(ipv4_addresses_lst)
    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus IPv4 addresses Converter
#
def _nexus_ipv4_converter(hostname:str(), cmd_outputs:list) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )


    for cmd_output in cmd_outputs:

        if 'TABLE_intf' in cmd_output.keys():

            if isinstance(cmd_output.get('TABLE_intf'), list):
                for interface in cmd_output.get('TABLE_intf'):
                    if isinstance(interface, dict):

                        ip_address = interface.get('ROW_intf').get('prefix', NOT_SET)

                        if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                                "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                                "::1/128" not in ip_address:

                            ipv4_obj = IPV4(
                                interface_name=_mapping_interface_name(interface.get('ROW_intf').get('intf-name')),
                                ip_address_with_mask=ip_address,
                                netmask=interface.get('ROW_intf').get('masklen')
                            )

                            ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

            elif isinstance(cmd_output.get('TABLE_intf'), dict):
                for interface, facts in cmd_output.get('TABLE_intf').items():

                    ip_address = facts.get('prefix', NOT_SET)

                    if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                            "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                            "::1/128" not in ip_address:
                        ipv4_obj = IPV4(
                            interface_name=_mapping_interface_name(facts.get('intf-name')),
                            ip_address_with_mask=ip_address,
                            netmask=facts.get('masklen')
                        )

                        ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS IPv4 addresses Converter
#
def _ios_ipv4_converter(hostname:str(), cmd_output:list) -> ListIPV4:
    
    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface in cmd_output:

        # In textfsm -> IPADDR & MASK are list
        # Value List IPADDR (\S+?)
        # Value List MASK (\d*)        
        for index, ip_addr in enumerate(interface[3]):
        
            ipv4_addresses_lst.ipv4_addresses_lst.append(
                IPV4(
                    interface_name=_mapping_interface_name(
                        interface[0]
                    ),
                    ip_address_with_mask=ip_addr,
                    netmask=interface[4][index]
                )
            )

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS XR IPv4 addresses Converter
#
def _iosxr_ipv4_converter(hostname:str(), cmd_output:list) -> ListIPV4:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista IPv4 addresses Converter
#
def _arista_ipv4_converter(hostname:str(), cmd_output:json) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface_name, facts in cmd_output.get('interfaces').items():

        ip_address = facts.get('interfaceAddress').get('primaryIp').get('address', NOT_SET)

        if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                "::1/128" not in ip_address:

            ipv4_obj = IPV4(
                interface_name=_mapping_interface_name(interface_name),
                ip_address_with_mask=ip_address,
                netmask=facts.get('interfaceAddress').get('primaryIp').get('maskLen', NOT_SET)
            )

            ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

    return ipv4_addresses_lst


# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper IPv4 addresses Converter
#
def _juniper_ipv4_converter(hostname:str(), cmd_output:list) -> ListIPV4:
    pass