#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.vrf_compare import _compare_transit_vrf
from netests.workers.arista_api import VRFAristaAPI
from netests.workers.arista_nc import VRFAristaNC
from netests.workers.arista_ssh import VRFAristaSSH
from netests.workers.cumulus_api import VRFCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import VRFCumulusSSH
from netests.workers.extreme_vsp_api import VRFExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import VRFExtremeVSPSSH
from netests.workers.ios_api import VRFIosAPI
from netests.workers.ios_nc import VRFIosNC
from netests.workers.ios_ssh import VRFIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import VRFIosxrNC
from netests.workers.iosxr_ssh import VRFIosxrSSH
from netests.workers.juniper_api import VRFJuniperAPI
from netests.workers.juniper_nc import VRFJuniperNC
from netests.workers.juniper_ssh import VRFJuniperSSH
from netests.workers.napalm_any import VRFNapalm
from netests.workers.nxos_api import VRFNxosAPI
from netests.workers.nxos_nc import VRFNxosNC
from netests.workers.nxos_ssh import VRFNxosSSH
from netests.getters.base_get import GetterBase


HEADER = "[netests - get_vrf]"


class GetterVRF(GetterBase):

    compare_function: str

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
        key_store
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
            key_store
        )
        self.init_mapping_function()

    def compare(self):
        log.debug(f"CALL _compare_transit_vrf num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_vrf,
            on_failed=True,
            num_workers=self.num_workers
        )
        super()._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFAristaAPI,
                self.NETCONF_CONNECTION: VRFAristaNC,
                self.SSH_CONNECTION: VRFAristaSSH,
                self.NAPALM_CONNECTION: VRFNapalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: VRFCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: VRFExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFIosAPI,
                self.NETCONF_CONNECTION: VRFIosNC,
                self.SSH_CONNECTION: VRFIosSSH,
                self.NAPALM_CONNECTION: VRFNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: VRFIosxrNC,
                self.SSH_CONNECTION: VRFIosxrSSH,
                self.NAPALM_CONNECTION: VRFNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFJuniperAPI,
                self.NETCONF_CONNECTION: VRFJuniperNC,
                self.SSH_CONNECTION: VRFJuniperSSH,
                self.NAPALM_CONNECTION: VRFNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFNxosAPI,
                self.NETCONF_CONNECTION: VRFNxosNC,
                self.SSH_CONNECTION: VRFNxosSSH,
                self.NAPALM_CONNECTION: VRFNapalm
            },
        }
