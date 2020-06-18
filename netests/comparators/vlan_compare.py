#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.protocols.vlan import VLAN, ListVLAN
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.constants import NOT_SET, VLAN_WORKS_KEY, VLAN_DATA_HOST_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_vlan(task, options={}):

    task.host[VLAN_WORKS_KEY] = _compare_vlan(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vlan_host_data=task.host.get(VLAN_DATA_HOST_KEY, None),
        test=False,
        options=options,
        task=task
    )

    return task.host[VLAN_WORKS_KEY]


def _compare_vlan(
    host_keys,
    hostname: str,
    groups: list,
    vlan_host_data: VLAN,
    test=False,
    options={},
    task=Task
) -> bool:
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            vlan_yaml_data = open_file(
                path="tests/features/src/vlan_tests.yml"
            ).get(hostname)
        else:
            vlan_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="vlan"
            )

        verity_vlan = ListVLAN(
            vlan_lst=list()
        )

        log.debug(
            "VLAN_DATA_HOST_KEY in host_keys="
            f"{VLAN_DATA_HOST_KEY in host_keys}\n"
            "vlan_yaml_data is not None="
            f"{vlan_yaml_data is not None}"
        )
        if (
            VLAN_DATA_HOST_KEY in host_keys and
            vlan_yaml_data is not None
        ):
            for vlan in vlan_yaml_data:

                ipv4 = IPV4Interface(ipv4_addresses=list())
                ipv6 = IPV6Interface(ipv6_addresses=list())

                for ip in vlan.get('ipv4_addresses', list()):
                    ipv4.ipv4_addresses.append(
                        IPV4(
                            ip_address=ip.get('ip_address'),
                            netmask=ip.get('netmasl')
                        )
                    )

                for ip in vlan.get('ipv6_addresses', list()):
                    ipv6.ipv6_addresses.append(
                        IPV6(
                            ip_address=ip.get('ip_address'),
                            netmask=ip.get('netmasl')
                        )
                    )

                verity_vlan.vlan_lst.append(
                    VLAN(
                        id=vlan.get('id', NOT_SET),
                        name=vlan.get('name', NOT_SET),
                        vrf_name=vlan.get('vrf_name', NOT_SET),
                        ipv4_addresses=ipv4,
                        ipv6_addresses=ipv6,
                        assigned_ports=vlan.get('assigned_ports'),
                    )
                )

            log_compare(verity_vlan, vlan_host_data, hostname, groups)
            return verity_vlan == vlan_host_data

        else:
            log_no_yaml_data(
                "vlan",
                VLAN_DATA_HOST_KEY,
                "VLAN_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
