#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.getters.routing_get import GetterRouting
from netests.comparators.isis_compare import _compare_transit_isis
from netests.workers.juniper_nc import ISISJuniperNC


class GetterISIS(GetterRouting):

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

    def compare(self):
        log.debug(f"CALL _compare_transit_isis num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_isis,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: ISISJuniperNC,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            }
        }
