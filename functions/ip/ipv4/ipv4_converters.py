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

def _generic_interface_filter(plateform, interface_name,*, get_vlan=True, get_loopback=True,
                              get_peerlink=True, get_vni=False, get_physical=True) -> bool:

    if "linux" in plateform and "bridge" not in interface_name and "v0" not in interface_name and \
            ((get_vlan and "vlan" in interface_name) or \
             (get_loopback and "lo" in interface_name) or \
             (get_peerlink and "peerlink" in interface_name) or \
             (get_vni and "vni" in interface_name) or \
             (get_physical and ("swp" in interface_name or "eth" in interface_name))):
        return True

    elif "nxos" in plateform and \
            ((get_vlan and "VLAN" in str(interface_name).upper()) or \
             (get_loopback and "LO" in str(interface_name).upper()) or \
             (get_physical and ("ETH" in str(interface_name).upper() or "MGMT" in str(interface_name).upper()))):
        return True

    elif "eos" in plateform and \
            ((get_vlan and "VLAN" in str(interface_name).upper()) or \
             (get_loopback and "LO" in str(interface_name).upper()) or \
             (get_physical and ("ETH" in str(interface_name).upper() or "MGMT" in str(interface_name).upper()))):
        return True

    return False
# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM IPv4 addresses converter
#
def _napalm_ipv4_converter(hostname:str(), plateform:str(), cmd_output:json, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:

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
def _cumulus_ipv4_converter(hostname:str(), plateform:str(), cmd_output:json, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface_name, facts in cmd_output.items():

        # v0 = vrrp / vrr / hsrp / HA ip address
        # bridge is a Linux bridge

        if _generic_interface_filter(
            plateform=plateform,
            interface_name=interface_name,
            get_vlan=get_vlan,
            get_loopback=get_loopback,
            get_peerlink=get_peerlink,
            get_vni=get_vni,
            get_physical=get_physical
        ):

            for ip_address_in_interface in facts.get("iface_obj").get('ip_address').get('allentries'):

                if "/128" not in ip_address_in_interface and "/64" not in ip_address_in_interface and \
                        "/48" not in ip_address_in_interface and "::" not in ip_address_in_interface and \
                        "127.0.0.1" not in ip_address_in_interface and "::1/128" not in ip_address_in_interface:

                    ipv4_obj = IPV4(
                        interface_name=_mapping_interface_name(
                            interface_name
                        ),
                        ip_address_with_mask=ip_address_in_interface
                    )

                    ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus IPv4 addresses Converter
#
def _nexus_ipv4_converter(hostname:str(), plateform:str(), cmd_outputs:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:

    if cmd_outputs is None:
        return False

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for cmd_output in cmd_outputs:

        if cmd_output is not None and 'TABLE_intf' in cmd_output.keys():

            if isinstance(cmd_output.get('TABLE_intf'), list):
                for interface in cmd_output.get('TABLE_intf'):
                    if _generic_interface_filter(
                        interface_name=_mapping_interface_name(
                            interface.get('ROW_intf').get('intf-name')
                        ),
                        plateform=plateform,
                        get_vlan=get_vlan,
                        get_peerlink=get_peerlink,
                        get_physical=get_physical,
                        get_loopback=get_loopback,
                        get_vni=get_vni
                    ):
                        if isinstance(interface, dict):

                            ip_address = interface.get('ROW_intf').get('prefix', NOT_SET)

                            if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                                    "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                                    "::1/128" not in ip_address:

                                ipv4_obj = IPV4(
                                    interface_name=_mapping_interface_name(
                                        interface.get('ROW_intf').get('intf-name')
                                    ),
                                    ip_address_with_mask=ip_address,
                                    netmask=interface.get('ROW_intf').get('masklen')
                                )

                                ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

                            if 'TABLE_secondary_address' in interface.get('ROW_intf').keys():
                                ipv4_addresses_lst.ipv4_addresses_lst.append(
                                    IPV4(
                                        interface_name=_mapping_interface_name(
                                            interface.get('ROW_intf').get('intf-name')
                                        ),
                                        ip_address_with_mask=interface.get('ROW_intf').get('TABLE_secondary_address').get(
                                            'ROW_secondary_address').get('prefix1'),
                                        netmask=interface.get('ROW_intf').get('TABLE_secondary_address').get(
                                            'ROW_secondary_address').get('masklen1')
                                    )
                                )

            elif isinstance(cmd_output.get('TABLE_intf'), dict):
                for interface, facts in cmd_output.get('TABLE_intf').items():
                    if _generic_interface_filter(
                            interface_name=_mapping_interface_name(
                                facts.get('intf-name')
                            ),
                            plateform=plateform,
                            get_vlan=get_vlan,
                            get_peerlink=get_peerlink,
                            get_physical=get_physical,
                            get_loopback=get_loopback,
                            get_vni=get_vni
                    ):
                        ip_address = facts.get('prefix', NOT_SET)

                        if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                                "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                                "::1/128" not in ip_address:
                            ipv4_obj = IPV4(
                                interface_name=_mapping_interface_name(
                                    facts.get('intf-name')
                                ),
                                ip_address_with_mask=ip_address,
                                netmask=facts.get('masklen')
                            )

                            ipv4_addresses_lst.ipv4_addresses_lst.append(ipv4_obj)

                        if 'TABLE_secondary_address' in facts.keys():
                            ipv4_addresses_lst.ipv4_addresses_lst.append(
                                IPV4(
                                    interface_name=_mapping_interface_name(
                                        facts.get('intf-name')
                                    ),
                                    ip_address_with_mask=facts.get('TABLE_secondary_address').get(
                                        'ROW_secondary_address').get('prefix1'),
                                    netmask=facts.get('TABLE_secondary_address').get('ROW_secondary_address').get(
                                        'masklen1')
                                )
                            )

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS IPv4 addresses Converter
#
def _ios_ipv4_converter(hostname:str(), plateform:str(), cmd_output:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:
    
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
def _iosxr_ipv4_converter(hostname:str(), plateform:str(), cmd_output:list, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista IPv4 addresses Converter
#
def _arista_ipv4_converter(hostname:str(), plateform:str(), cmd_output:json, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for interface_name, facts in cmd_output.get('interfaces').items():
        if _generic_interface_filter(
                interface_name=_mapping_interface_name(
                    interface_name
                ),
                plateform=plateform,
                get_vlan=get_vlan,
                get_peerlink=get_peerlink,
                get_physical=get_physical,
                get_loopback=get_loopback,
                get_vni=get_vni
        ):
            ip_address = facts.get('interfaceAddress').get('primaryIp').get('address', NOT_SET)

            if ip_address != NOT_SET and "/128" not in ip_address and "/64" not in ip_address and \
                    "/48" not in ip_address and "::" not in ip_address and "127.0.0.1" not in ip_address and \
                    "::1/128" not in ip_address:

                ipv4_addresses_lst.ipv4_addresses_lst.append(
                    IPV4(
                        interface_name=_mapping_interface_name(
                            interface_name
                        ),
                        ip_address_with_mask=ip_address,
                        netmask=facts.get('interfaceAddress').get('primaryIp').get('maskLen', NOT_SET)
                    )
                )

            if len(facts.get('interfaceAddress').get('secondaryIpsOrderedList')) > 0:

                for ip_addr in facts.get('interfaceAddress').get('secondaryIpsOrderedList'):
                    secondary_ip = ip_addr.get('address', NOT_SET)

                    if secondary_ip != NOT_SET and "/128" not in secondary_ip and "/64" not in secondary_ip and \
                            "/48" not in secondary_ip and "::" not in secondary_ip and "127.0.0.1" not in secondary_ip and \
                            "::1/128" not in secondary_ip:

                        ipv4_addresses_lst.ipv4_addresses_lst.append(
                            IPV4(
                                interface_name=_mapping_interface_name(
                                    interface_name
                                ),
                                ip_address_with_mask=secondary_ip,
                                netmask=ip_addr.get('maskLen', NOT_SET)
                            )
                        )

    print(ipv4_addresses_lst)
    return ipv4_addresses_lst


# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper IPv4 addresses Converter
#
def _juniper_ipv4_converter(hostname:str(), plateform:str(), cmd_output:dict, *, get_vlan=True, get_loopback=True,
                            get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:

    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for key in cmd_output.get('interface-information')[0].keys():
        if key != "attributes":
            for interface in cmd_output.get('interface-information')[0].get(key):
                if "logical-interface" in interface.keys():
                    for logic_interface in interface.get("logical-interface"):
                        if "address-family" in logic_interface.keys():
                            if "address-family-name" in logic_interface.get("address-family")[0]:
                                if logic_interface.get("address-family")[0].get("address-family-name")[0].get("data") == "inet" and \
                                        logic_interface.get("address-family")[0].get("interface-address") is not None:

                                    for interface_ip in logic_interface.get("address-family")[0].get("interface-address"):

                                        ip_addr = interface_ip.get("ifa-local")[0].get("data", NOT_SET)

                                        if ip_addr != NOT_SET and \
                                                "/128" not in ip_addr and \
                                                "/64" not in ip_addr and \
                                                "/48" not in ip_addr and \
                                                "::" not in ip_addr and \
                                                "127.0.0.1" not in ip_addr and \
                                                "::1/128" not in ip_addr and \
                                                "128.0.0." not in ip_addr and \
                                                ".32768" not in logic_interface.get("name")[0].get("data", NOT_SET):

                                            if "lo" in logic_interface.get("name")[0].get("data", NOT_SET) :
                                                ipv4_addresses_lst.ipv4_addresses_lst.append(
                                                    IPV4(
                                                        interface_name=_mapping_interface_name(
                                                            logic_interface.get("name")[0].get("data",NOT_SET)
                                                        ),
                                                        ip_address_with_mask=ip_addr,
                                                        netmask="255.255.255.255"
                                                    )
                                                )
                                            else:
                                                ipv4_addresses_lst.ipv4_addresses_lst.append(
                                                    IPV4(
                                                        interface_name=_mapping_interface_name(
                                                            logic_interface.get("name")[0].get("data", NOT_SET)
                                                        ),
                                                        ip_address_with_mask=ip_addr,
                                                    )
                                                )

    return ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Networks VSP IPv4 addresses Converter
#
def _extreme_vsp_ipv4_converter(hostname: str(), plateform:str(), cmd_output: dict, *, get_vlan=True, get_loopback=True,
                                get_peerlink=True, get_vni=False, get_physical=True) -> ListIPV4:
    
    ipv4_addresses_lst = ListIPV4(
        hostname=hostname,
        ipv4_addresses_lst=list()
    )

    for vrf in cmd_output:
        
        for interface in cmd_output.get(vrf):
            
            ipv4_addresses_lst.ipv4_addresses_lst.append(
                IPV4(
                    interface_name=_mapping_interface_name(
                        interface[0]
                    ),
                    ip_address_with_mask=interface[1],
                    netmask=interface[2]
                )
            )

    return ipv4_addresses_lst
