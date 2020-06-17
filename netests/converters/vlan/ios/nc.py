#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.vlan import ListVLAN


def _ios_vlan_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListVLAN:

    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    print(cmd_output)

    return vlan_lst
