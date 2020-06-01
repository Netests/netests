#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.cdp_compare import _compare_transit_cdp
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
from netests.workers.juniper_api import CDPJuniperAPI
from netests.workers.juniper_nc import CDPJuniperNC
from netests.workers.juniper_ssh import CDPJuniperSSH
from netests.workers.napalm_any import CDPNapalm
from netests.workers.nxos_api import CDPNxosAPI
from netests.workers.nxos_nc import CDPNxosNC
from netests.workers.nxos_ssh import CDPNxosSSH


class GetterCDP(GetterBase):

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
        log.debug(f"CALL _compare_transit_cdp  num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_cdp,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPAristaAPI,
                self.NETCONF_CONNECTION: CDPAristaNC,
                self.SSH_CONNECTION: CDPAristaSSH,
                self.NAPALM_CONNECTION: CDPNapalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: CDPCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: CDPExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPIosAPI,
                self.NETCONF_CONNECTION: CDPIosNC,
                self.SSH_CONNECTION: CDPIosSSH,
                self.NAPALM_CONNECTION: CDPNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: CDPIosxrNC,
                self.SSH_CONNECTION: CDPIosxrSSH,
                self.NAPALM_CONNECTION: CDPNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPJuniperAPI,
                self.NETCONF_CONNECTION: CDPJuniperNC,
                self.SSH_CONNECTION: CDPJuniperSSH,
                self.NAPALM_CONNECTION: CDPNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: CDPNxosAPI,
                self.NETCONF_CONNECTION: CDPNxosNC,
                self.SSH_CONNECTION: CDPNxosSSH,
                self.NAPALM_CONNECTION: CDPNapalm
            }
        }
