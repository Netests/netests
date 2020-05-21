#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.base_get import GetterBase
from netests.workers.arista_api import CDPAristaAPI
from netests.workers.arista_ssh import CDPAristaSSH
from netests.workers.cumulus_api import CDPCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import CDPCumulusSSH
from netests.constants import CDP_DATA_HOST_KEY

HEADER = "[netests - get_cdp]"


class GetterCDP(GetterBase):

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
        self.print_protocols_result(CDP_DATA_HOST_KEY, "CDP")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPAristaAPI,                
                self.NETCONF_CONNECTION: "pass",
                self.SSH_CONNECTION: CDPAristaSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: CDPCumulusSSH,
                self.NAPALM_CONNECTION: "pass"
            }
        }
