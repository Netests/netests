#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.ospf import OSPF, ListOSPFSessionsVRF


def _ios_ospf_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ListOSPFSessionsVRF(
            ospf_sessions_vrf_lst=list()
        )
    )
