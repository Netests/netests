#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.converters.bgp.nxos.ssh import _nxos_bgp_ssh_converter
from netests.converters.cdp.nxos.ssh import _nxos_cdp_ssh_converter
from netests.converters.facts.nxos.ssh import _nxos_facts_ssh_converter
from netests.converters.lldp.nxos.ssh import _nxos_lldp_ssh_converter
from netests.converters.ospf.nxos.ssh import _nxos_ospf_ssh_converter
from netests.converters.vrf.nxos.ssh import _nxos_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    NEXUS_GET_BGP,
    NEXUS_GET_BGP_VRF,
    NEXUS_GET_CDP,
    NEXUS_GET_FACTS,
    NEXUS_GET_INT,
    NEXUS_GET_DOMAIN,
    NEXUS_GET_LLDP,
    NEXUS_GET_OSPF,
    NEXUS_GET_OSPF_RID,
    NEXUS_GET_OSPF_VRF,
    NEXUS_GET_OSPF_RID_VRF,
    NEXUS_GET_VRF
)


class BGPNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_GET_BGP,
                },
                "vrf": {
                    "no_key": NEXUS_GET_BGP_VRF,
                },
            },
            vrf_loop=True,
            converter=_nxos_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_GET_CDP
                }
            },
            vrf_loop=False,
            converter=_nxos_cdp_ssh_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": NEXUS_GET_FACTS,
                    "get_infos_int": NEXUS_GET_INT,
                    "get_infos_domain": NEXUS_GET_DOMAIN
                }
            },
            vrf_loop=False,
            converter=_nxos_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_nxos_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "data": NEXUS_GET_OSPF,
                    "rid": NEXUS_GET_OSPF_RID
                },
                "vrf": {
                    "data": NEXUS_GET_OSPF_VRF,
                    "rid": NEXUS_GET_OSPF_RID_VRF
                },
            },
            vrf_loop=True,
            converter=_nxos_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFNxosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
