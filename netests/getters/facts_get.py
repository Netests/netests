#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.facts_compare import _compare_transit_facts
from netests.getters.base_get import GetterBase
from netests.constants import FACTS_DATA_HOST_KEY
from netests.workers.arista_api import FactsAristaAPI
from netests.workers.arista_nc import FactsAristaNC
from netests.workers.arista_ssh import FactsAristaSSH
from netests.workers.cumulus_api import FactsCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import FactsCumulusSSH
from netests.workers.extreme_vsp_api import FactsExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import FactsExtremeVSPSSH
from netests.workers.ios_api import FactsIosAPI
from netests.workers.ios_nc import FactsIosNC
from netests.workers.ios_ssh import FactsIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import FactsIosxrNC
from netests.workers.iosxr_ssh import FactsIosxrSSH
from netests.workers.juniper_api import FactsJuniperAPI
from netests.workers.juniper_nc import FactsJuniperNC
from netests.workers.juniper_ssh import FactsJuniperSSH
from netests.workers.napalm_any import FactsNapalm
from netests.workers.nxos_api import FactsNxosAPI
from netests.workers.nxos_nc import FactsNxosNC
from netests.workers.nxos_ssh import FactsNxosSSH


HEADER = "[netests - get_facts]"


class GetterFacts(GetterBase):

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
            key_store,
        )
        self.init_mapping_function()

    def compare(self):
        log.debug(
            f"CALL _compare_transit_facts num_workers={self.num_workers}"
        )
        data = self.devices.run(
            task=_compare_transit_facts,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def print_result(self):
        self.print_protocols_result(FACTS_DATA_HOST_KEY, "Facts")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsAristaAPI,
                self.NETCONF_CONNECTION: FactsAristaNC,
                self.SSH_CONNECTION: FactsAristaSSH,
                self.NAPALM_CONNECTION: FactsNapalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: FactsCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: FactsExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsIosAPI,
                self.NETCONF_CONNECTION: FactsIosNC,
                self.SSH_CONNECTION: FactsIosSSH,
                self.NAPALM_CONNECTION: FactsNapalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: FactsIosxrNC,
                self.SSH_CONNECTION: FactsIosxrSSH,
                self.NAPALM_CONNECTION: FactsNapalm
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsJuniperAPI,
                self.NETCONF_CONNECTION: FactsJuniperNC,
                self.SSH_CONNECTION: FactsJuniperSSH,
                self.NAPALM_CONNECTION: FactsNapalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsNxosAPI,
                self.NETCONF_CONNECTION: FactsNxosNC,
                self.SSH_CONNECTION: FactsNxosSSH,
                self.NAPALM_CONNECTION: FactsNapalm
            }
        }
