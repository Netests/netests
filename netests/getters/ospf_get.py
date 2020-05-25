#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.routing_get import GetterRouting
from netests.constants import OSPF_SESSIONS_HOST_KEY
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
from netests.workers.nxos_api import OSPFNxosAPI
from netests.workers.nxos_nc import OSPFNxosNC
from netests.workers.nxos_ssh import OSPFNxosSSH

HEADER = "[netests - get_ospf]"


class GetterOSPF(GetterRouting):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output,
        compare
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output,
            compare
        )
        self.init_mapping_function()

    def run(self):
        self.get_vrf()
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def print_result(self):
        self.print_protocols_result(OSPF_SESSIONS_HOST_KEY, "OSPF")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFAristaAPI,
                self.NETCONF_CONNECTION: OSPFAristaNC,
                self.SSH_CONNECTION: OSPFAristaSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
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
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: OSPFIosxrNC,
                self.SSH_CONNECTION: OSPFIosxrSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: OSPFNxosAPI,
                self.NETCONF_CONNECTION: OSPFNxosNC,
                self.SSH_CONNECTION: OSPFNxosSSH,
                self.NAPALM_CONNECTION: "pass"
            }
        }
