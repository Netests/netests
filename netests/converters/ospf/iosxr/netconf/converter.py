
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)


def _iosxr_ospf_netconf_converter(
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
