#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from jnpr.junos import Device
from netests.workers.device_nc import DeviceNC
from netests.converters.bgp.juniper.nc import _juniper_bgp_nc_converter
from netests.converters.facts.juniper.nc import _juniper_facts_nc_converter
from netests.converters.lldp.juniper.nc import _juniper_lldp_nc_converter
from netests.converters.ospf.juniper.nc import _juniper_ospf_nc_converter
from netests.converters.vrf.juniper.nc import _juniper_vrf_nc_converter
from netests.exceptions.netests_exceptions import NetestsFunctionNotPossible
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY
)


class JuniperNC(DeviceNC, ABC):

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
        source='running',
        format_command=False
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options,
            format_command
        )
        if nc_method == 'get' or nc_method == 'get_config':
            self.nc_method = nc_method
        else:
            self.nc_method = 'get'
        self.source = source

    def exec_call(self, task, command, vrf):
        if self.nc_method == 'get':
            return self.exec_call_get(task, command, vrf)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command, vrf)

    def exec_call_get(self, task, command, vrf):
        return self.__exec_call_generic(task, command, vrf)

    def exec_call_get_config(self, task, command, vrf):
        return self.__exec_call_generic(task, command, vrf)

    def __exec_call_generic(self, task, command, vrf):
        with Device(
            host=task.host.hostname,
            port=task.host.port,
            user=task.host.username,
            passwd=task.host.password,
        ) as m:
            vrf_config = self.format_rpc_output(command(m, vrf))
            self.validate_xml(vrf_config)
            return vrf_config

    def _mapping_get_instance_information(self, m, vrf):
        return m.rpc.get_instance_information(detail=True)

    def _mapping_get_ospf_neighbor_information(self, m, vrf):
        return m.rpc.get_ospf_neighbor_information(detail=True, instance=vrf)

    def _mapping_get_ospf_overview_information(self, m, vrf):
        return m.rpc.get_ospf_overview_information(instance=vrf)

    def _mapping_get_bgp_neighbor_information(self, m, vrf):
        return m.rpc.get_bgp_neighbor_information(exact_instance=vrf)

    def _mapping_get_instance_information_bgp(self, m, vrf):
        return m.rpc.get_instance_information(
            detail=True,
            instance_name=vrf
        )

    def _mapping_get_lldp_neighbors_information(self, m, vrf):
        return m.rpc.get_lldp_neighbors_information()

    def _mapping_facts(self, m, vrf):
        a = dict(m.facts)
        return a

    def _mapping_transit_facts(self, m, vrf):
        return self._mapping_facts(m, vrf)

    def _mapping_get_interface_information(self, m, vrf):
        return m.rpc.get_interface_information(terse=True)


class BGPJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "bgp": self._mapping_get_bgp_neighbor_information,
                    "rid": self._mapping_get_instance_information_bgp
                },
                "vrf": {
                    "bgp": self._mapping_get_bgp_neighbor_information,
                    "rid": self._mapping_get_instance_information_bgp
                }
            },
            vrf_loop=True,
            converter=_juniper_bgp_nc_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            nc_method='get',
            options=options,
            source='running',
            format_command=False
        )


class CDPJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        raise NetestsFunctionNotPossible(
            "Juniper doesn't support CDP"
        )


class FactsJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "get_infos_sys": self._mapping_transit_facts,
                    "get_infos_int": self._mapping_get_interface_information
                },
            },
            vrf_loop=False,
            converter=_juniper_facts_nc_converter,
            key_store=FACTS_DATA_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class LLDPJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self._mapping_get_lldp_neighbors_information
                }
            },
            vrf_loop=False,
            converter=_juniper_lldp_nc_converter,
            key_store=LLDP_DATA_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class OSPFJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "data": self._mapping_get_ospf_neighbor_information,
                    "rid": self._mapping_get_ospf_overview_information
                },
                "vrf": {
                    "data": self._mapping_get_ospf_neighbor_information,
                    "rid": self._mapping_get_ospf_overview_information
                }
            },
            vrf_loop=True,
            converter=_juniper_ospf_nc_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            nc_method='get',
            options=options,
            source='running',
            format_command=False
        )


class VRFJuniperNC(JuniperNC):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self._mapping_get_instance_information
                }
            },
            vrf_loop=False,
            converter=_juniper_vrf_nc_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get',
            options=options,
            source='running'
        )
