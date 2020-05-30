#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.workers.device_ssh import DeviceSSH
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.converters.bgp.extreme_vsp.ssh import (
    _extreme_vsp_bgp_ssh_converter
)
from netests.converters.facts.extreme_vsp.ssh import (
    _extreme_vsp_facts_ssh_converter
)
from netests.converters.lldp.extreme_vsp.ssh import (
    _extreme_vsp_lldp_ssh_converter
)
from netests.converters.ospf.extreme_vsp.ssh import (
    _extreme_vsp_ospf_ssh_converter
    )
from netests.converters.vrf.extreme_vsp.ssh import (
    _extreme_vsp_vrf_ssh_converter
)
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    EXTREME_VSP_GET_BGP,
    EXTREME_VSP_GET_BGP_VRF,
    EXTREME_VSP_GET_FACTS,
    EXTREME_VSP_GET_INT,
    EXTREME_VSP_GET_DOMAIN,
    EXTREME_VSP_GET_LLDP,
    EXTREME_VSP_GET_OSPF,
    EXTREME_VSP_GET_OSPF_RID,
    EXTREME_VSP_GET_OSPF_INTERFACES,
    EXTREME_VSP_GET_OSPF_VRF,
    EXTREME_VSP_GET_OSPF_RID_VRF,
    EXTREME_VSP_GET_OSPF_INTERFACES_VRF,
    EXTREME_VSP_GET_VRF
)


class BGPExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": EXTREME_VSP_GET_BGP
                },
                "vrf": {
                    "no_key": EXTREME_VSP_GET_BGP_VRF
                }
            },
            vrf_loop=True,
            converter=_extreme_vsp_bgp_ssh_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "ExtremeVSP doesn't support CDP"
        )


class FactsExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": EXTREME_VSP_GET_FACTS,
                    "get_infos_int": EXTREME_VSP_GET_INT,
                    "get_infos_domain": EXTREME_VSP_GET_DOMAIN,
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_facts_ssh_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": EXTREME_VSP_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_lldp_ssh_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "rid": EXTREME_VSP_GET_OSPF_RID,
                    "data": EXTREME_VSP_GET_OSPF,
                    "int": EXTREME_VSP_GET_OSPF_INTERFACES
                },
                "vrf": {
                    "rid": EXTREME_VSP_GET_OSPF_RID_VRF,
                    "data": EXTREME_VSP_GET_OSPF_VRF,
                    "int": EXTREME_VSP_GET_OSPF_INTERFACES_VRF
                }
            },
            vrf_loop=True,
            converter=_extreme_vsp_ospf_ssh_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFExtremeVSPSSH(DeviceSSH):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": EXTREME_VSP_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_extreme_vsp_vrf_ssh_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
