#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.ospf import ListOSPFSessionsVRF, OSPF


def _arista_ospf_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )
