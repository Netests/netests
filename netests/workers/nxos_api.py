#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from netests import log
from netests.workers.device_api import DeviceAPI
from netests.converters.bgp.nxos.api import _nxos_bgp_api_converter
from netests.converters.cdp.nxos.api import _nxos_cdp_api_converter
from netests.converters.facts.nxos.api import _nxos_facts_api_converter
from netests.converters.lldp.nxos.api import _nxos_lldp_api_converter
from netests.converters.ospf.nxos.api import _nxos_ospf_api_converter
from netests.converters.vrf.nxos.api import _nxos_vrf_api_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    NEXUS_API_GET_BGP,
    NEXUS_API_GET_BGP_VRF,
    NEXUS_API_GET_CDP,
    NEXUS_API_GET_FACTS,
    NEXUS_API_GET_INT,
    NEXUS_API_GET_DOMAIN,
    NEXUS_API_GET_LLDP,
    NEXUS_API_GET_OSPF,
    NEXUS_API_GET_OSPF_RID,
    NEXUS_API_GET_OSPF_VRF,
    NEXUS_API_GET_OSPF_RID_VRF,
    NEXUS_API_GET_VRF
)


class NxosAPI(DeviceAPI, ABC):

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
        p = self.use_https(task.host.get('secure_api', True))

        log.debug(
            "\n"
            f"CALL exec_call for Cisco NXOS\n"
            f"method=POST\n"
            f"auth=requests.auth.HTTPBasicAuth(username, password)\n"
            f"endpoint={p}://{task.host.hostname}:{task.host.port}/ins\n"
            f"headers='Content-Type': 'application/json'\n"
            """data={
                "ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": "%s",
                    "output_format": "json"
                }
            }""" % (str(command))
        )

        res = requests.post(
            url=f"{p}://{task.host.hostname}:{task.host.port}/ins",
            headers={
                'Content-Type': 'application/json',
            },
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False,
            data="""{
                "ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": "%s",
                    "output_format": "json"
                }
            }""" % (str(command))
        )
        self.check_status_code(res.status_code)

        log.debug(
            "\n"
            f"RESULT exec_call for Cisco NXOS\n"
            f"status_code={res.status_code}\n"
            f"content={res.content}\n"
        )

        return res.content


class BGPNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_API_GET_BGP,
                },
                "vrf": {
                    "no_key": NEXUS_API_GET_BGP_VRF,
                },
            },
            vrf_loop=True,
            converter=_nxos_bgp_api_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            options=options
        )


class CDPNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_API_GET_CDP
                }
            },
            vrf_loop=False,
            converter=_nxos_cdp_api_converter,
            key_store=CDP_DATA_HOST_KEY,
            options=options
        )


class FactsNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": NEXUS_API_GET_FACTS,
                    "get_infos_int": NEXUS_API_GET_INT,
                    "get_infos_domain": NEXUS_API_GET_DOMAIN
                }
            },
            vrf_loop=False,
            converter=_nxos_facts_api_converter,
            key_store=FACTS_DATA_HOST_KEY,
            options=options
        )


class LLDPNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_API_GET_LLDP
                }
            },
            vrf_loop=False,
            converter=_nxos_lldp_api_converter,
            key_store=LLDP_DATA_HOST_KEY,
            options=options
        )


class OSPFNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "data": NEXUS_API_GET_OSPF,
                    "rid": NEXUS_API_GET_OSPF_RID
                },
                "vrf": {
                    "data": NEXUS_API_GET_OSPF_VRF,
                    "rid": NEXUS_API_GET_OSPF_RID_VRF
                },
            },
            vrf_loop=True,
            converter=_nxos_ospf_api_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )


class VRFNxosAPI(NxosAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": NEXUS_API_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
