#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.base_get import GetterBase
from netests.workers.arista_api import LLDPAristaAPI
from netests.workers.arista_nc import LLDPAristaNC
from netests.workers.arista_ssh import LLDPAristaSSH
from netests.workers.cumulus_api import LLDPCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import LLDPCumulusSSH
from netests.workers.extreme_vsp_api import LLDPExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import LLDPExtremeVSPSSH
from netests.workers.ios_ssh import LLDPIosSSH

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
                self.NETCONF_CONNECTION: LLDPAristaNC,
                self.SSH_CONNECTION: LLDPAristaSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: LLDPCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: LLDPExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: "",
                self.NETCONF_CONNECTION: "",
                self.SSH_CONNECTION: LLDPIosSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
