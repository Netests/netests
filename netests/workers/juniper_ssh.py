#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.converters.bgp.juniper.ssh import _juniper_bgp_ssh_converter
from netests.converters.facts.juniper.ssh import _juniper_facts_ssh_converter
from netests.converters.lldp.juniper.ssh import _juniper_lldp_ssh_converter
from netests.converters.ospf.juniper.ssh import _juniper_ospf_ssh_converter
from netests.converters.vrf.juniper.ssh import _juniper_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    JUNOS_GET_BGP,
    JUNOS_GET_BGP_RID,
    JUNOS_GET_BGP_VRF,
    JUNOS_GET_BGP_VRF_RID,
    JUNOS_GET_FACTS,
    JUNOS_GET_INT,
    JUNOS_GET_MEMORY,
    JUNOS_GET_CONFIG_SYSTEM,
    JUNOS_GET_SERIAL,
    JUNOS_GET_LLDP,
    JUNOS_GET_OSPF_NEI,
    JUNOS_GET_OSPF_RID,
    JUNOS_GET_OSPF_NEI_VRF,
    JUNOS_GET_OSPF_RID_VRF,
    JUNOS_GET_VRF_DETAIL
)


class BGPJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "data": JUNOS_GET_BGP,
                    "rid": JUNOS_GET_BGP_RID
                },
                "vrf": {
                    "data": JUNOS_GET_BGP_VRF,
                    "rid": JUNOS_GET_BGP_VRF_RID
                },
            },
            vrf_loop=True,
            converter=_juniper_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Juniper doesn't support CDP"
        )


class FactsJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": JUNOS_GET_FACTS,
                    "get_infos_int": JUNOS_GET_INT,
                    "get_infos_memory": JUNOS_GET_MEMORY,
                    "get_infos_config": JUNOS_GET_CONFIG_SYSTEM,
                    "get_infos_serial": JUNOS_GET_SERIAL
                }
            },
            vrf_loop=False,
            converter=_juniper_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": JUNOS_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_juniper_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "data": JUNOS_GET_OSPF_NEI,
                    "rid": JUNOS_GET_OSPF_RID
                },
                "vrf": {
                    "data": JUNOS_GET_OSPF_NEI_VRF,
                    "rid": JUNOS_GET_OSPF_RID_VRF
                },
            },
            vrf_loop=True,
            converter=_juniper_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFJuniperSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": JUNOS_GET_VRF_DETAIL
                }
            },
            vrf_loop=False,
            converter=_juniper_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
