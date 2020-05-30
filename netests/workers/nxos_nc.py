#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests import log
from ncclient import manager
from netests.workers.device_nc import DeviceNC
from netests.exceptions.netests_exceptions import NetestsFunctionNotImplemented
from netests.converters.vrf.nxos.nc import _nxos_vrf_nc_converter
from netests.constants import VRF_DATA_KEY


class NxosNC(DeviceNC, ABC):

    nc_method: str
    source: str

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        nc_method,
        options={},
        source='running'
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )
        if nc_method == 'get' or nc_method == 'get_config':
            self.nc_method = nc_method
        else:
            self.nc_method = 'get'
        self.source = source

    def exec_call(self, task, command, vrf):
        log.debug(f"nc method for ({task.host.name}) = {self.nc_method}")

        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    def exec_call_get(self, task, command):
        pass

    def exec_call_get_config(self, task, command):
        log.debug(
            f"CALL Netconf function for NXOS\n"
            f"hostname={task.host.hostname}\n"
            f"port={task.host.port}\n"
            "hostkey_verify=False\n"
            "device_params={'name': 'nexus'}\n"
            f"command={command}\n"
            f"source={self.source}\n"
            "Use Filter with 'subtree'\n"
        )

        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False,
            device_params={'name': 'nexus'}
        ) as m:

            data = m.get_config(
                source=self.source,
                filter=(
                    'subtree',
                    (
                        command
                    )
                )
            ).data_xml
            self.validate_xml(data)

            log.debug(
                f"RESULT Netconf function for NXOS\n"
                f"hostname={task.host.hostname}\n"
                f"port={task.host.port}\n"
                "hostkey_verify=False\n"
                "device_params={'name': 'nexus'}\n"
                f"command={command}\n"
                f"source={self.source}\n"
                "Use Filter with 'subtree'\n"
                f"==> {data}"
            )
            return data


class BGPNxosNC(NxosNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco NXOS - BGP - Netconf - Not Possible"
        )


class CDPNxosNC(NxosNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco NXOS - CDP - Netconf - Not Possible"
        )


class FactsNxosNC(NxosNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco NXOS - Facts - Netconf - Not Possible"
        )


class LLDPNxosNC(NxosNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco NXOS - LLDP - Netconf - Not Possible"
        )


class OSPFNxosNC(NxosNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco NXOS - OSPF - Netconf - Not Possible"
        )


class VRFNxosNC(NxosNC):

    NETCONF_FILTER = """
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <inst-items/>
        </System>"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_nc_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )
