#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.converters.bgp.arista.ssh import _arista_bgp_ssh_converter
from netests.converters.facts.arista.ssh import _arista_facts_ssh_converter
from netests.converters.lldp.arista.ssh import _arista_lldp_ssh_converter
from netests.converters.ospf.arista.ssh import _arista_ospf_ssh_converter
from netests.converters.vrf.arista.ssh import _arista_vrf_ssh_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    ARISTA_GET_BGP,
    ARISTA_GET_BGP_VRF,
    ARISTA_GET_FACTS,
    ARISTA_GET_INT,
    ARISTA_GET_DOMAIN,
    ARISTA_GET_LLDP,
    ARISTA_GET_OSPF,
    ARISTA_GET_OSPF_RID,
    ARISTA_GET_OSPF_VRF,
    ARISTA_GET_OSPF_RID_VRF,
    ARISTA_GET_VRF
)


class BGPAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_GET_BGP
                },
                "vrf": {
                    "no_key": ARISTA_GET_BGP_VRF
                }
            },
            vrf_loop=True,
            converter=_arista_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Arista doesn't support CDP"
        )


class FactsAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": ARISTA_GET_FACTS,
                    "get_infos_int": ARISTA_GET_INT,
                    "get_infos_domain": ARISTA_GET_DOMAIN,
                }
            },
            vrf_loop=False,
            converter=_arista_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_arista_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "rid": ARISTA_GET_OSPF_RID,
                    "data": ARISTA_GET_OSPF
                },
                "vrf": {
                    "rid": ARISTA_GET_OSPF_RID_VRF,
                    "data": ARISTA_GET_OSPF_VRF
                }
            },
            vrf_loop=True,
            converter=_arista_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFAristaSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": ARISTA_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_arista_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
