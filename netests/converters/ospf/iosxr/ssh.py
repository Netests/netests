#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.ospf import ListOSPFSessionsVRF, OSPF


def _iosxr_ospf_ssh_converter(
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
