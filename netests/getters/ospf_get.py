#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.ospf_compare import _compare_transit_ospf
from netests.getters.routing_get import GetterRouting
from netests.workers.arista_api import OSPFAristaAPI
from netests.workers.arista_nc import OSPFAristaNC
from netests.workers.arista_ssh import OSPFAristaSSH
from netests.workers.cumulus_api import OSPFCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import OSPFCumulusSSH
from netests.workers.extreme_vsp_api import OSPFExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import OSPFExtremeVSPSSH
from netests.workers.ios_api import OSPFIosAPI
from netests.workers.ios_nc import OSPFIosNC
from netests.workers.ios_ssh import OSPFIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import OSPFIosxrNC
from netests.workers.iosxr_ssh import OSPFIosxrSSH
from netests.workers.juniper_api import OSPFJuniperAPI
from netests.workers.juniper_nc import OSPFJuniperNC
from netests.workers.juniper_ssh import OSPFJuniperSSH
from netests.workers.napalm_any import OSPFNapalm
from netests.workers.nxos_api import OSPFNxosAPI
from netests.workers.nxos_nc import OSPFNxosNC
from netests.workers.nxos_ssh import OSPFNxosSSH


class GetterOSPF(GetterRouting):

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
        log.debug(f"CALL _compare_transit_ospf num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_ospf,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFAristaAPI,
                self.NETCONF_CONNECTION: OSPFAristaNC,
                self.SSH_CONNECTION: OSPFAristaSSH,
                self.NAPALM_CONNECTION: OSPFNapalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: OSPFCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: OSPFExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFIosAPI,
                self.NETCONF_CONNECTION: OSPFIosNC,
                self.SSH_CONNECTION: OSPFIosSSH,
                self.NAPALM_CONNECTION: OSPFNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: OSPFIosxrNC,
                self.SSH_CONNECTION: OSPFIosxrSSH,
                self.NAPALM_CONNECTION: OSPFNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFJuniperAPI,
                self.NETCONF_CONNECTION: OSPFJuniperNC,
                self.SSH_CONNECTION: OSPFJuniperSSH,
                self.NAPALM_CONNECTION: OSPFNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFNxosAPI,
                self.NETCONF_CONNECTION: OSPFNxosNC,
                self.SSH_CONNECTION: OSPFNxosSSH,
                self.NAPALM_CONNECTION: OSPFNapalm
            }
        }
