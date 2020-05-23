#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import CDP_DATA_HOST_KEY
from netests.getters.base_get import GetterBase
from netests.workers.arista_api import CDPAristaAPI
from netests.workers.arista_nc import CDPAristaNC
from netests.workers.arista_ssh import CDPAristaSSH
from netests.workers.cumulus_api import CDPCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import CDPCumulusSSH
from netests.workers.extreme_vsp_api import CDPExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import CDPExtremeVSPSSH
from netests.workers.ios_api import CDPIosAPI
from netests.workers.ios_nc import CDPIosNC
from netests.workers.ios_ssh import CDPIosSSH


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
                self.NETCONF_CONNECTION: CDPAristaNC,
                self.SSH_CONNECTION: CDPAristaSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: CDPCumulusSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: CDPExtremeVSPSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPIosAPI,
                self.NETCONF_CONNECTION: CDPIosNC,
                self.SSH_CONNECTION: CDPIosSSH,
                self.NAPALM_CONNECTION: "pass"
            }
        }
