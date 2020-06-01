#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests import log
from netests.workers.device import Device
from nornir.plugins.tasks.networking import napalm_get
from netests.converters.bgp.napalm.converter import _napalm_bgp_converter
from netests.converters.facts.napalm.converter import _napalm_facts_converter
from netests.converters.lldp.napalm.converter import _napalm_lldp_converter
from netests.converters.vrf.napalm.converter import _napalm_vrf_converter
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.constants import (
    VRF_DATA_KEY,
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
)


class NapalmAny(Device, ABC):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={},
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )

    def exec_call(self, task, command, vrf):
        log.debug(
            "\n"
            "Execute a Nornir NAPALM get (napalm_get) :\n"
            f"commands={command}\n"
        )
        output = task.run(
            name=f"NAPALM Execute {command}",
            task=napalm_get,
            getters=[f"{command}"],
        )
        log.debug(
            "\n"
            "Result a Nornir NAPALM get (napalm_get) :\n"
            f"output={output.result}\n"
        )
        return output.result


class BGPNapalm(NapalmAny):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get_bgp_neighbors"
                }
            },
            vrf_loop=False,
            converter=_napalm_bgp_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPNapalm(NapalmAny):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "NAPALM - CDP - Not Possible"
        )


class FactsNapalm(NapalmAny):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "facts"
                }
            },
            vrf_loop=False,
            converter=_napalm_facts_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPNapalm(NapalmAny):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get_lldp_neighbors_detail"
                }
            },
            vrf_loop=False,
            converter=_napalm_lldp_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFNapalm(NapalmAny):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "NAPALM - OSPF - Not Possible"
        )


class VRFNapalm(NapalmAny):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get_network_instances"
                }
            },
            vrf_loop=False,
            converter=_napalm_vrf_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
