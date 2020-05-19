#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from jnpr.junos import Device
from functions.workers.device_nc import DeviceNC
from const.constants import VRF_DATA_KEY
from functions.converters.vrf.juniper.netconf.converter import _juniper_vrf_netconf_converter


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

    def exec_call(self, task, command):
        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    def exec_call_get(self, task, command):
        return self.__exec_call_genetic(task, command)

    def exec_call_get_config(self, task, command):
        return self.__exec_call_genetic(task, command)

    def __exec_call_genetic(self, task, command):
        with Device(
            host=task.host.hostname,
            port=task.host.port,
            user=task.host.username,
            passwd=task.host.password,
        ) as m:

            vrf_config = self.format_rpc_output(command(m))
            self.validate_xml(vrf_config)
            return vrf_config

    def _mapping_get_instance_information(self, m):
        return m.rpc.get_instance_information(detail=True)


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
            converter=_juniper_vrf_netconf_converter,
            key_store=VRF_DATA_KEY,
            options=options,
            source='running'
        )
