#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.converters.bgp.cumulus.ssh import _cumulus_bgp_ssh_converter
from netests.converters.cdp.cumulus.ssh import _cumulus_cdp_ssh_converter
from netests.converters.facts.cumulus.ssh import _cumulus_facts_ssh_converter
from netests.converters.lldp.cumulus.ssh import _cumulus_lldp_ssh_converter
from netests.converters.ospf.cumulus.ssh import _cumulus_ospf_ssh_converter
from netests.converters.vrf.cumulus.ssh import _cumulus_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    CUMULUS_GET_BGP,
    CUMULUS_GET_BGP_VRF,
    CUMULUS_GET_LLDP_CDP,
    CUMULUS_GET_FACTS,
    CUMULUS_GET_INT,
    CUMULUS_GET_OSPF,
    CUMULUS_GET_OSPF_RID,
    CUMULUS_GET_OSPF_VRF,
    CUMULUS_GET_OSPF_RID_VRF,
    CUMULUS_GET_VRF
)


class BGPCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_GET_BGP
                },
                "vrf": {
                    "no_key": CUMULUS_GET_BGP_VRF
                }
            },
            vrf_loop=True,
            converter=_cumulus_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_GET_LLDP_CDP
                }
            },
            vrf_loop=False,
            converter=_cumulus_cdp_ssh_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": CUMULUS_GET_FACTS,
                    "get_infos_int": CUMULUS_GET_INT
                }
            },
            vrf_loop=False,
            converter=_cumulus_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_GET_LLDP_CDP
                }
            },
            vrf_loop=False,
            converter=_cumulus_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "rid": CUMULUS_GET_OSPF_RID,
                    "data": CUMULUS_GET_OSPF
                },
                "vrf": {
                    "rid": CUMULUS_GET_OSPF_RID_VRF,
                    "data": CUMULUS_GET_OSPF_VRF
                }
            },
            vrf_loop=True,
            converter=_cumulus_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFCumulusSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
