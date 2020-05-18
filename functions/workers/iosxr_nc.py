#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from ncclient import manager
from functions.workers.device_nc import DeviceNC
from const.constants import ARISTA_GET_VRF, VRF_DATA_KEY, VRF_DEFAULT_RT_LST
from functions.converters.vrf.iosxr.netconf.converter import _iosxr_vrf_netconf_converter


class IosxrNC(DeviceNC, ABC):

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
        pass

    def exec_call_get_config(self, task, command):
        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False,
            device_params={'name': 'iosxr'}
        ) as m:

            vrf_config = m.get_config(
                source=self.source,
                filter=(
                    'subtree',
                    (
                        command
                    )
                )
            ).data_xml
            self.validate_xml(vrf_config)
            return vrf_config


class VRFIosxrNC(IosxrNC):

    NETCONF_FILTER_VRF = """
        <vrfs
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-infra-rsi-cfg\"
        />"""

    NETCONF_FILTER_BGP = """
        <bgp
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "VRF": self.NETCONF_FILTER_VRF,
                    "BGP": self.NETCONF_FILTER_BGP
                }
            },
            vrf_loop=False,
            converter=_iosxr_vrf_netconf_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )
