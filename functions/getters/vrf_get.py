#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.workers.arista_api import VRFAristaAPI
from functions.workers.arista_nc import VRFAristaNC
from functions.workers.arista_ssh import VRFAristaSSH
from functions.workers.cumulus_ssh import VRFCumulusSSH
from functions.workers.cumulus_api import VRFCumulusAPI
from functions.workers.extreme_vsp_api import VRFExtremeVSPAPI
from functions.workers.extreme_vsp_nc import ExtremeVSPNC
from functions.workers.extreme_vsp_ssh import VRFExtremeVSPSSH
from functions.workers.ios_api import VRFIosAPI
from functions.workers.ios_nc import VRFIosNC
from functions.workers.ios_ssh import VRFIosSSH
from functions.workers.iosxr_api import IosxrAPI
from functions.workers.iosxr_nc import VRFIosxrNC
from functions.workers.iosxr_ssh import VRFIosxrSSH
from functions.workers.juniper_ssh import VRFJuniperSSH
from functions.workers.nxos_api import VRFNxosAPI
from functions.workers.nxos_nc import VRFNxosNC
from functions.workers.nxos_ssh import VRFNxosSSH
from functions.getters.base_get import GetterBase
from const.constants import VRF_DATA_KEY, VRF_NAME_DATA_KEY


HEADER = "[netests - get_vrf]"


class GetterVRF(GetterBase):

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

    def print_result(self):
        self.print_protocols_result(VRF_DATA_KEY, "VRF")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFAristaAPI,
                self.NETCONF_CONNECTION: VRFAristaNC,
                self.SSH_CONNECTION: VRFAristaSSH
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFCumulusAPI,
                self.SSH_CONNECTION: VRFCumulusSSH,
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: VRFExtremeVSPSSH
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFIosAPI,
                self.NETCONF_CONNECTION: VRFIosNC,
                self.SSH_CONNECTION: VRFIosSSH
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: VRFIosxrNC,
                self.SSH_CONNECTION: VRFIosxrSSH
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.SSH_CONNECTION: VRFJuniperSSH
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: VRFNxosAPI,
                self.NETCONF_CONNECTION: VRFNxosNC,
                self.SSH_CONNECTION: VRFNxosSSH
            },
        }
