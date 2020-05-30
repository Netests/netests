#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.converters.bgp.juniper.api import _juniper_bgp_api_converter
from netests.converters.facts.juniper.api import _juniper_facts_api_converter
from netests.converters.lldp.juniper.api import _juniper_lldp_api_converter
from netests.converters.ospf.juniper.api import _juniper_ospf_api_converter
from netests.converters.vrf.juniper.api import _juniper_vrf_api_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY
)


class JuniperAPI(DeviceAPI, ABC):

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
        protocol = self.use_https(task.host.get('secure_api', True))

        res = requests.get(
            url=(
                f"{protocol}://{task.host.hostname}:{task.host.port}"
                f"/rpc/{command}"
            ),
            headers={'content-type': 'application/xml'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )
        self.check_status_code(res.status_code)
        return res.content


class BGPJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "bgp":
                        "get-bgp-neighbor-information?exact-instance=master",
                    "rid":
                        "get-instance-information?instance-name=master&detail="
                },
                "vrf": {
                    "bgp": "get-bgp-neighbor-information?exact-instance={}",
                    "rid": "get-instance-information?instance-name={}&detail="
                }
            },
            vrf_loop=True,
            converter=_juniper_bgp_api_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Juniper doesn't support CDP"
        )


class FactsJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": "get-software-information",
                    "get_infos_int": "get-interface-information?terse=",
                    "get_infos_serial": "get-chassis-inventory?detail=",
                    "get_infos_memory": "get-system-memory-information"
                },
            },
            vrf_loop=False,
            converter=_juniper_facts_api_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get-lldp-neighbors-information"
                },
            },
            vrf_loop=False,
            converter=_juniper_lldp_api_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "bgp":
                       "get-ospf-neighbor-information?instance=master&detail=",
                    "rid": "get-ospf-overview-information?instance=master"
                },
                "vrf": {
                    "bgp":
                        "get-ospf-neighbor-information?instance={}&detail=",
                    "rid": "get-ospf-overview-information?instance={}"
                }
            },
            vrf_loop=True,
            converter=_juniper_ospf_api_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFJuniperAPI(JuniperAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "get-instance-information?detail="
                }
            },
            vrf_loop=False,
            converter=_juniper_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
