#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.bgp_compare import _compare_transit_bgp
from netests.getters.routing_get import GetterRouting
from netests.workers.arista_api import BGPAristaAPI
from netests.workers.arista_nc import BGPAristaNC
from netests.workers.arista_ssh import BGPAristaSSH
from netests.workers.cumulus_api import BGPCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import BGPCumulusSSH
from netests.workers.extreme_vsp_api import BGPExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import BGPExtremeVSPSSH
from netests.workers.ios_api import BGPIosAPI
from netests.workers.ios_nc import BGPIosNC
from netests.workers.ios_ssh import BGPIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import BGPIosxrNC
from netests.workers.iosxr_ssh import BGPIosxrSSH
from netests.workers.juniper_api import BGPJuniperAPI
from netests.workers.juniper_nc import BGPJuniperNC
from netests.workers.juniper_ssh import BGPJuniperSSH
from netests.workers.napalm_any import BGPNapalm
from netests.workers.nxos_api import BGPNxosAPI
from netests.workers.nxos_nc import BGPNxosNC
from netests.workers.nxos_ssh import BGPNxosSSH


class GetterBGP(GetterRouting):

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
        log.debug(f"CALL _compare_transit_bgp  num_workers={self.num_workers}")
        data = self.devices.run(
            task=_compare_transit_bgp,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPAristaAPI,
                self.NETCONF_CONNECTION: BGPAristaNC,
                self.SSH_CONNECTION: BGPAristaSSH,
                self.NAPALM_CONNECTION: BGPNapalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: BGPCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: BGPExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPIosAPI,
                self.NETCONF_CONNECTION: BGPIosNC,
                self.SSH_CONNECTION: BGPIosSSH,
                self.NAPALM_CONNECTION: BGPNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: BGPIosxrNC,
                self.SSH_CONNECTION: BGPIosxrSSH,
                self.NAPALM_CONNECTION: BGPNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPJuniperAPI,
                self.NETCONF_CONNECTION: BGPJuniperNC,
                self.SSH_CONNECTION: BGPJuniperSSH,
                self.NAPALM_CONNECTION: BGPNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPNxosAPI,
                self.NETCONF_CONNECTION: BGPNxosNC,
                self.SSH_CONNECTION: BGPNxosSSH,
                self.NAPALM_CONNECTION: BGPNapalm
            }
        }
