#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.base_get import GetterBase
from netests.workers.arista_api import LLDPAristaAPI
from netests.constants import LLDP_DATA_HOST_KEY

HEADER = "[netests - get_lldp]"


class GetterLLDP(GetterBase):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output
        )
        self.init_mapping_function()

    def run(self):
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def print_result(self):
        self.print_protocols_result(LLDP_DATA_HOST_KEY, "LLDP")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPAristaAPI,
                self.SSH_CONNECTION: "pass",
                self.NETCONF_CONNECTION: "pass",
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
