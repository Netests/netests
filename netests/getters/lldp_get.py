#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.lldp_compare import _compare_transit_lldp
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
from netests.workers.ios_api import LLDPIosAPI
from netests.workers.ios_nc import LLDPIosNC
from netests.workers.ios_ssh import LLDPIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import LLDPIosxrNC
from netests.workers.iosxr_ssh import LLDPIosxrSSH
from netests.workers.juniper_api import LLDPJuniperAPI
from netests.workers.juniper_nc import LLDPJuniperNC
from netests.workers.juniper_ssh import LLDPJuniperSSH
from netests.workers.napalm_any import LLDPNapalm
from netests.workers.nxos_api import LLDPNxosAPI
from netests.workers.nxos_nc import LLDPNxosNC
from netests.workers.nxos_ssh import LLDPNxosSSH


class GetterLLDP(GetterBase):

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
        log.debug(f"CALL _compare_transit_lldp num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_lldp,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPAristaAPI,
                self.NETCONF_CONNECTION: LLDPAristaNC,
                self.SSH_CONNECTION: LLDPAristaSSH,
                self.NAPALM_CONNECTION: LLDPNapalm
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
                self.API_CONNECTION: LLDPIosAPI,
                self.NETCONF_CONNECTION: LLDPIosNC,
                self.SSH_CONNECTION: LLDPIosSSH,
                self.NAPALM_CONNECTION: LLDPNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: LLDPIosxrNC,
                self.SSH_CONNECTION: LLDPIosxrSSH,
                self.NAPALM_CONNECTION: LLDPNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPJuniperAPI,
                self.NETCONF_CONNECTION: LLDPJuniperNC,
                self.SSH_CONNECTION: LLDPJuniperSSH,
                self.NAPALM_CONNECTION: LLDPNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: LLDPNxosAPI,
                self.NETCONF_CONNECTION: LLDPNxosNC,
                self.SSH_CONNECTION: LLDPNxosSSH,
                self.NAPALM_CONNECTION: LLDPNapalm
            }
        }
