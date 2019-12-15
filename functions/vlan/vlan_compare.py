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
ERROR_HEADER = "Error import [vlan_compare.py]"
HEADER_GET = "[netests - compare_vlan]"

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
def compare_vlan(nr, vlan_yaml_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_vlan,
        vlan_yaml_data=vlan_yaml_data,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

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
def _compare_transit_vlan(task, vlan_yaml_data:json):

    task.host[VLAN_WORKS_KEY] = _compare_vlan(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        vlan_host_data=task.host[VLAN_DATA_HOST_KEY],
        vlan_yaml_data=vlan_yaml_data,
    )

    return task.host[VLAN_WORKS_KEY]

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_vlan(host_keys, hostname, vlan_host_data:None, vlan_yaml_data:json) -> bool:

    if vlan_yaml_data is None:
        return False

    verity_vlans_lst = ListVLAN(
        vlans_lst=list()
    )

    if VLAN_DATA_HOST_KEY in host_keys and hostname in vlan_yaml_data.keys():
        for vlan in vlan_yaml_data.get(hostname):

            fhrp_ip = "0.0.0.0"
            ipv4_addresses_lst = ListIPV4(
                ipv4_addresses_lst=list()
            )

            ipv6_addresses_lst = ListIPV6(
                ipv6_addresses_lst=list()
            )


            if "ip_address" in vlan.keys():
                if isinstance(vlan.get("ip_address"), list):
                    for ip_address in vlan.get("ip_address"):
                        index_slash = str(ip_address).find("/")
                        ipv4_addresses_lst.ipv4_addresses_lst.append(
                            IPV4(
                                ip_address_with_mask=str(ip_address)[:index_slash],
                                netmask=str(ip_address)[index_slash+1:]
                            )
                        )
                elif isinstance(vlan.get("ip_address"), str):
                    index_slash = str(vlan.get("ip_address")).find("/")
                    ipv4_addresses_lst.ipv4_addresses_lst.append(
                        IPV4(
                            ip_address_with_mask=str(vlan.get("ip_address"))[:index_slash],
                            netmask=str(vlan.get("ip_address"))[index_slash + 1:]
                        )
                    )

            if "ipv6_address" in vlan.keys():
                if isinstance(vlan.get("ipv6_address"), list):
                    for ipv6_address in vlan.get("ipv6_address"):
                        ipv6_addresses_lst.ipv6_addresses_lst.append(
                            IPV6(
                                ip_address_with_mask=str(ipv6_address),
                            )
                        )
                elif isinstance(vlan.get("ip_address"), str):
                    ipv6_addresses_lst.ipv6_addresses_lst.append(
                        IPV6(
                            ip_address_with_mask=str(vlan.get("ip_address"))
                        )
                    )

            verity_vlans_lst.vlans_lst.append(
                VLAN(
                    vlan_name=vlan.get("vlan_name", NOT_SET),
                    vlan_id=vlan.get("vlan_id", NOT_SET),
                    vlan_descr=vlan.get("vlan_descr", NOT_SET),
                    vrf_name=vlan.get("vrf_name", NOT_SET),
                    ipv6_addresses=ipv6_addresses_lst,
                    ipv4_addresses=ipv4_addresses_lst,
                    fhrp_ip_address=vlan.get("fhrp_ip_address", "0.0.0.0"),
                    ports_members=vlan.get("ports_members", list()),
                    mac_address=vlan.get("mac_address", NOT_SET)

                )
            )

        return verity_vlans_lst == vlan_host_data

    else:
        print(f"[{HEADER_GET}] {hostname} is not present in {PATH_TO_VERITY_FILES}/{TEST_TO_EXC_VLAN_KEY}.")
        return False



