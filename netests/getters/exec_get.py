#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.getters.base_get import GetterBase
from netests.converters.ping.arista.api import _arista_ping_api_exec
from netests.converters.ping.ping_execute import _execute_netmiko_ping_cmd
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
            num_workers=10
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
        )(task, self.options)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: _arista_ping_api_exec,
                self.NETCONF_CONNECTION: "",
                self.SSH_CONNECTION: _execute_netmiko_ping_cmd,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
