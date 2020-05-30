#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.exceptions.netests_exceptions import NetestsFunctionNotImplemented
from netests.converters.bgp.iosxr.ssh import _iosxr_bgp_ssh_converter
from netests.converters.cdp.iosxr.ssh import _iosxr_cdp_ssh_converter
from netests.converters.facts.iosxr.ssh import _iosxr_facts_ssh_converter
from netests.converters.lldp.iosxr.ssh import _iosxr_lldp_ssh_converter
from netests.converters.vrf.iosxr.ssh import _iosxr_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    VRF_DATA_KEY,
    IOSXR_GET_BGP_PEERS,
    IOSXR_GET_BGP_RID,
    IOSXR_VRF_GET_BGP_PEERS,
    IOSXR_VRF_GET_BGP_RID,
    IOSXR_GET_CDP,
    IOSXR_GET_FACTS,
    IOSXR_GET_INT,
    IOSXR_GET_LLDP,
    IOSXR_GET_VRF
)


class BGPIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "peers": IOSXR_GET_BGP_PEERS,
                    "rid": IOSXR_GET_BGP_RID
                },
                "vrf": {
                    "peers": IOSXR_VRF_GET_BGP_PEERS,
                    "rid": IOSXR_VRF_GET_BGP_RID
                },
            },
            vrf_loop=True,
            converter=_iosxr_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOSXR_GET_CDP
                }
            },
            vrf_loop=False,
            converter=_iosxr_cdp_ssh_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": IOSXR_GET_FACTS,
                    "get_infos_int": IOSXR_GET_INT
                }
            },
            vrf_loop=False,
            converter=_iosxr_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOSXR_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_iosxr_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco IOS-XR - SSH - OSPF not implemented"
        )


class VRFIosxrSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOSXR_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_iosxr_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
