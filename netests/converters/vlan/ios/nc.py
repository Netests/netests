#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.vlan import VLAN, ListVLAN
from netests.constants import NOT_SET


def _ios_vlan_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> VLAN:

    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    print(cmd_output)


    return vlan_lst
