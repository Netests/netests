#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [ipv6_compare.py]"
HEADER_GET = "[netests - compare_ipv6]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

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
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#

def compare_ipv6(nr, ipv6_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_ipv6,
        ipv6_yaml_data=ipv6_yaml_data,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(f"{HEADER_GET} Task '_compare' has failed for {value.host} (value.result={value.result}).")
            return_value = False

    return (not data.failed and return_value)

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare Transit function
#
def _compare_transit_ipv6(task, ipv6_yaml_data:json):

    task.host[IPV6_WORKS_KEY] = _compare_ipv6(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        ipv6_host_data=task.host[IPV6_DATA_HOST_KEY],
        ipv6_yaml_data=ipv6_yaml_data,
    )

    return task.host[IPV6_WORKS_KEY]


# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_ipv6(host_keys, hostname:str, groups:list, ipv6_host_data:ListIPV6, ipv6_yaml_data:dict) -> bool:

    verity_ipv6 = retrieve_ipv6_for_host(
        hostname=hostname,
        groups=groups,
        ipv6_yaml_data=ipv6_yaml_data
    )

    return verity_ipv6 == ipv6_host_data


# ----------------------------------------------------------------------------------------------------------------------
#
#
def retrieve_ipv6_for_host(hostname:str, groups, ipv6_yaml_data:dict) -> ListIPV6:

    ip_addresses_lst = ListIPV6(
        hostname=hostname,
        ipv6_addresses_lst=list()
    )

    # Retrieve data in "all:"
    if YAML_ALL_GROUPS_KEY in ipv6_yaml_data.keys():
        for ip_infos in ipv6_yaml_data.get(YAML_ALL_GROUPS_KEY, NOT_SET):

            ipv6_obj = IPV6(
                interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                netmask=ip_infos.get('netmask', NOT_SET),
            )

            ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)


    # Retrieve data in "groups:"
    if YAML_GROUPS_KEY in ipv6_yaml_data.keys():
        for value_key_groups in ipv6_yaml_data.get(YAML_GROUPS_KEY, NOT_SET).keys():
            for host_group in groups:
                if "," in value_key_groups:
                    if host_group in value_key_groups.split(","):
                        for ip_infos in ipv6_yaml_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            ipv6_obj = IPV6(
                                interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                                ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                                netmask=ip_infos.get('netmask', NOT_SET),
                            )

                            ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)

                else:
                    if host_group == value_key_groups:
                        for ip_infos in ipv6_yaml_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            ipv6_obj = IPV6(
                                interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                                ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                                netmask=ip_infos.get('netmask', NOT_SET),
                            )

                            ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)

    # Retrieve data in "devices:"
    if YAML_DEVICES_KEY in ipv6_yaml_data.keys():
        for value_key_devices in ipv6_yaml_data.get(YAML_DEVICES_KEY, NOT_SET).keys():
            if "," in value_key_devices:
                if hostname in value_key_devices.split(","):
                    for ip_infos in ipv6_yaml_data.get(YAML_DEVICES_KEY, NOT_SET).get(value_key_devices, NOT_SET):

                        ipv6_obj = IPV6(
                            interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                            ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                            netmask=ip_infos.get('netmask', NOT_SET),
                        )

                        ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)

            else:
                if hostname == value_key_devices:

                    for ip_infos in ipv6_yaml_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_devices):

                        ipv6_obj = IPV6(
                            interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                            ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                            netmask=ip_infos.get('netmask', NOT_SET),
                        )

                        ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)


    # Retrieve data per device
    if hostname in ipv6_yaml_data.keys():

        for ip_infos in ipv6_yaml_data.get(hostname, NOT_SET):
            ipv6_obj = IPV6(
                interface_name=_mapping_interface_name(ip_infos.get('interface_name', NOT_SET)),
                ip_address_with_mask=ip_infos.get('ip_address', NOT_SET),
                netmask=ip_infos.get('netmask', NOT_SET),
            )

            ip_addresses_lst.ipv6_addresses_lst.append(ipv6_obj)

    return ip_addresses_lst