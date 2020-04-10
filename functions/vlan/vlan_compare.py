#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from nornir.core.task import Task
from nornir.plugins.functions.text import print_result
from functions.verbose_mode import verbose_mode
from functions.select_vars import select_host_vars
from functions.global_tools import open_file
from protocols.vlan import VLAN, ListVLAN
from protocols.ipv4 import IPV4, ListIPV4
from protocols.ipv6 import (
    IPV6,
    ListIPV6,
    IPV6Interface,
    ListIPV6Interface
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    VLAN_DATA_HOST_KEY,
    VLAN_WORKS_KEY
)
from functions.discovery_protocols.discovery_functions import (
    _mapping_interface_name
)


HEADER = "[netests - vlan_compare]"


def compare_vlan(nr, own_vars={}) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_vlan,
        on_failed=True,
        own_vars=own_vars,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(
                f"{HEADER} Task '_compare' has failed for {value.host}"
                f"(value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_vlan(task, own_vars={}):
    task.host[VLAN_WORKS_KEY] = _compare_vlan(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vlan_host_data=task.host[VLAN_DATA_HOST_KEY],
        test=False,
        own_vars=own_vars,
        task=task
    )

    return task.host[VLAN_WORKS_KEY]


def _compare_vlan(
    host_keys,
    hostname: str,
    groups: list,
    vlan_host_data: ListVLAN,
    test:False,
    own_vars={},
    task=Task
) -> bool:
    verity_vlans_lst = ListVLAN(vlans_lst=list())

    if test:
        vlan_yaml_data = open_file(
            path="tests/features/src/vlan_tests.yml"
        )
    else:
        vlan_yaml_data = select_host_vars(
            hostname=hostname,
            groups=groups,
            protocol="vlan"
        )
    
    if VLAN_DATA_HOST_KEY in host_keys and hostname in vlan_yaml_data.keys():
        for vlan in vlan_yaml_data.get(hostname):
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


            ports_members = list()
            if "ports_members" in vlan.keys():
                for port in vlan.get("ports_members"):
                    ports_members.append(
                        _mapping_interface_name(
                            port
                        )
                    )

            verity_vlans_lst.vlans_lst.append(
                VLAN(
                    vlan_name=vlan.get("vlan_name", NOT_SET),
                    vlan_id=vlan.get("vlan_id", NOT_SET),
                    vlan_descr=vlan.get("vlan_descr", NOT_SET),
                    vrf_name=vlan.get("vrf_name", NOT_SET),
                    ipv6_addresses=ipv6_addresses_lst,
                    fhrp_ipv6_address=vlan.get("fhrp_ipv6_address", "0.0.0.0"),
                    ipv4_addresses=ipv4_addresses_lst,
                    fhrp_ipv4_address=vlan.get("fhrp_ipv4_address", "0.0.0.0"),
                    ports_members=ports_members,
                    mac_address=vlan.get("mac_address", NOT_SET)
                )
            )

        return verity_vlans_lst == vlan_host_data

    else:
        print(f"{HEADER}Key {VLAN_DATA_HOST_KEY} is missing for {hostname}")
        return False



