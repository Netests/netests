#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from netests import log
from ncclient import manager
from netests.workers.device_nc import DeviceNC
from netests.exceptions.netests_exceptions import NetestsFunctionNotImplemented
from netests.converters.bgp.iosxr.nc import _iosxr_bgp_nc_converter
from netests.converters.vrf.iosxr.nc import _iosxr_vrf_nc_converter
from netests.constants import BGP_SESSIONS_HOST_KEY, VRF_DATA_KEY


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

    def exec_call(self, task, command, vrf):
        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    def exec_call_get(self, task, command):
        pass

    def exec_call_get_config(self, task, command):
        log.debug(
            f"CALL Netconf function for IOSXR\n"
            f"hostname={task.host.hostname}\n",
            f"port={task.host.port}\n",
            "hostkey_verify=False\n"
            "device_params={'name': 'iosxr'}\n"
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
            device_params={'name': 'iosxr'}
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
                f"RESULT Netconf function for IOSXR\n"
                f"hostname={task.host.hostname}\n",
                f"port={task.host.port}\n",
                "hostkey_verify=False\n"
                "device_params={'name': 'iosxr'}\n"
                f"command={command}\n"
                f"source={self.source}\n"
                "Use Filter with 'subtree'\n"
                f"==> {data}"
            )

            return data


class BGPIosxrNC(IosxrNC):

    NETCONF_FILTER = """
        <bgp
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "BGP": self.NETCONF_FILTER_BGP
                }
            },
            vrf_loop=False,
            converter=_iosxr_bgp_nc_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )


class CDPIosxrNC(IosxrNC):
    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco IOS-XR - Netconf - CDP not implemented"
        )


class FactsIosxrNC(IosxrNC):
    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco IOS-XR - Netconf - Facts not implemented"
        )


class LLDPIosxrNC(IosxrNC):
    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco IOS-XR - Netconf - LLDP not implemented"
        )


class OSPFIosxrNC(IosxrNC):
    def __init__(self, task, options={}):
        raise NetestsFunctionNotImplemented(
            "Cisco IOS-XR - Netconf - OSPF not implemented"
        )


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
            converter=_iosxr_vrf_nc_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )
