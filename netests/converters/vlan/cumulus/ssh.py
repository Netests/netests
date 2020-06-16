#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.vlan import VLAN, ListVLAN
from netests.constants import NOT_SET


def _cumulus_vlan_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> VLAN:

    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    if cmd_output is not None:
        if not isinstance(cmd_output, dict):
            cmd_output = json.loads(cmd_output)

        for key, value in cmd_output.items():
            if 'vlan' in key:
                ipv4_addresses = IPV4Interface(ipv4_addresses=list())
                ipv6_addresses = IPV6Interface(ipv6_addresses=list())

                if len(
                    value.get('iface_obj').get('ip_address').get('allentries')
                ) > 0:
                    for ip in value.get('iface_obj') \
                                   .get('ip_address') \
                                   .get('allentries'):
                        if ':' in ip:
                            # Is an IPv6 (light I know :)
                            ipv6_addresses.ipv6_addresses.append(
                                IPV6(
                                    ip_address=ip.split('/')[0],
                                    netmask=ip.split('/')[1]
                                )
                            )
                        else:
                            ipv4_addresses.ipv4_addresses.append(
                                IPV4(
                                    ip_address=ip.split('/')[0],
                                    netmask=ip.split('/')[1]
                                )
                            )

                vlan_lst.vlan_lst.append(
                    VLAN(
                        id=key[4:],
                        name=value.get('iface_obj')
                                  .get('description', NOT_SET),
                        vrf_name=NOT_SET,
                        ipv4_addresses=ipv4_addresses,
                        ipv6_addresses=ipv6_addresses,
                        assigned_port=[],
                        options=options
                    )
                )

    return vlan_lst
