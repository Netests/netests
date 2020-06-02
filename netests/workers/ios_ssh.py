#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.converters.bgp.ios.ssh import _ios_bgp_ssh_converter
from netests.converters.cdp.ios.ssh import _ios_cdp_ssh_converter
from netests.converters.facts.ios.ssh import _ios_facts_ssh_converter
from netests.converters.lldp.ios.ssh import _ios_lldp_ssh_converter
from netests.converters.ospf.ios.ssh import _ios_ospf_ssh_converter
from netests.converters.vrf.ios.ssh import _ios_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    IOS_GET_BGP,
    IOS_GET_BGP_VRF,
    IOS_GET_CDP,
    IOS_GET_FACTS,
    IOS_GET_INT,
    IOS_GET_LLDP,
    IOS_GET_OSPF_NEI,
    IOS_GET_OSPF,
    IOS_GET_OSPF_INT,
    IOS_GET_VRF
)


class BGPIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOS_GET_BGP
                },
                "vrf": {
                    "no_key": IOS_GET_BGP_VRF
                }
            },
            vrf_loop=True,
            converter=_ios_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOS_GET_CDP
                }
            },
            vrf_loop=False,
            converter=_ios_cdp_ssh_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": IOS_GET_FACTS,
                    "get_infos_int": IOS_GET_INT
                }
            },
            vrf_loop=False,
            converter=_ios_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOS_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_ios_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "int": IOS_GET_OSPF_INT,
                    "data": IOS_GET_OSPF_NEI,
                    "rid": IOS_GET_OSPF
                }
            },
            vrf_loop=True,
            converter=_ios_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFIosSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": IOS_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_ios_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
