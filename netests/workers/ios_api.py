#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.converters.bgp.ios.api import _ios_bgp_api_converter
from netests.converters.cdp.ios.api import _ios_cdp_api_converter
from netests.converters.facts.ios.api import _ios_facts_api_converter
from netests.converters.lldp.ios.api import _ios_lldp_api_converter
from netests.converters.ospf.ios.api import _ios_ospf_api_converter
from netests.converters.vrf.ios.api import _ios_vrf_api_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY
)


class IosAPI(DeviceAPI, ABC):

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
                f"/restconf/data/{command}"
            ),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False,
            data={}
        )
        self.check_status_code(res.status_code)
        return res.content


class BGPIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-bgp-oper:bgp-state-data"
                }
            },
            vrf_loop=False,
            converter=_ios_bgp_api_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-cdp-oper:cdp-neighbor-details"
                }
            },
            vrf_loop=False,
            converter=_ios_cdp_api_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-native:native"
                }
            },
            vrf_loop=False,
            converter=_ios_facts_api_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-lldp-oper:lldp-entries"
                }
            },
            vrf_loop=False,
            converter=_ios_lldp_api_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-ospf-oper:ospf-oper-data"
                }
            },
            vrf_loop=False,
            converter=_ios_ospf_api_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFIosAPI(IosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": "Cisco-IOS-XE-native:native"
                }
            },
            vrf_loop=False,
            converter=_ios_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
