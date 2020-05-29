#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.cdp_compare import _compare_transit_cdp
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
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import CDPIosxrNC
from netests.workers.iosxr_ssh import CDPIosxrSSH
from netests.workers.nxos_api import CDPNxosAPI
from netests.workers.nxos_nc import CDPNxosNC
from netests.workers.nxos_ssh import CDPNxosSSH


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

    def compare(self):
        log.debug(f"CALL _compare_transit_cdp  num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_cdp,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

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
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: CDPIosxrNC,
                self.SSH_CONNECTION: CDPIosxrSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPNxosAPI,
                self.NETCONF_CONNECTION: CDPNxosNC,
                self.SSH_CONNECTION: CDPNxosSSH,
                self.NAPALM_CONNECTION: "pass"
            }
        }
