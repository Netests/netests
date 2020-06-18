#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.comparators.vlan_compare import _compare_transit_vlan
from netests.getters.base_get import GetterBase
from netests.constants import VLAN_DATA_HOST_KEY
from netests.workers.cumulus_ssh import VLANCumulusSSH
from netests.workers.ios_nc import VLANIosNC
from netests.workers.ios_ssh import VLANIosSSH

HEADER = "[netests - get_vlan]"


class GetterVLAN(GetterBase):

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
            task=_compare_transit_vlan,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)

    def print_result(self):
        self.print_protocols_result(VLAN_DATA_HOST_KEY, "vlan")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: VLANCumulusSSH,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: VLANIosNC,
                self.SSH_CONNECTION: VLANIosSSH,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: self.function_not_implemented,
                self.NETCONF_CONNECTION: self.function_not_implemented,
                self.SSH_CONNECTION: self.function_not_implemented,
                self.NAPALM_CONNECTION: self.function_not_implemented
            }
        }
