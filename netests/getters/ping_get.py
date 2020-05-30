#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.getters.base_get import GetterBase

from netests.converters.ping.arista.api import _arista_ping_api_exec
from netests.converters.ping.iosxr.nc import _iosxr_ping_nc_exec
from netests.converters.ping.juniper.nc import _juniper_ping_nc_exec
from netests.converters.ping.juniper.api import _juniper_ping_api_exec
from netests.converters.ping.nxos.api import _nxos_ping_api_exec
from netests.converters.ping.ping_execute import (
    _execute_netmiko_ping_cmd,
    _execute_linux_ping_cmd
)
from netests.comparators.ping_retrieve import (
    retrieve_ping_from_yaml,
    _generic_generate_ping_cmd
)


class GetterPing(GetterBase):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output,
        filename,
        protocol,
        key_store,
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output,
            filename,
            protocol,
            key_store,
        )
        self.init_mapping_function()

    def run(self):
        log.debug("Run <retrieve_ping_from_yaml>")
        self.devices.run(
            task=retrieve_ping_from_yaml,
            on_failed=True,
            num_workers=self.num_workers
        )

        self.devices.run(
            task=_generic_generate_ping_cmd,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def compare(self):
        data = self.devices.run(
            task=self.execute_ping,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def execute_ping(self, task):
        return self.base_selection(
            platform=task.host.platform,
            connection_mode=task.host.data.get("connexion"),
            functions_mapping=self.MAPPING_FUNCTION
        )(task)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: _arista_ping_api_exec,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: _execute_linux_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: _iosxr_ping_nc_exec,
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: _juniper_ping_api_exec,
                self.NETCONF_CONNECTION: _juniper_ping_nc_exec,
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: _nxos_ping_api_exec,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: _execute_linux_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
