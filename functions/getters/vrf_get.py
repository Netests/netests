#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.getters.base_get import GetterBase
from functions.vrf.arista.vrf_arista import (
    _arista_get_vrf_api,
    _arista_get_vrf_netconf,
    _arista_get_vrf_ssh
)
from functions.vrf.cumulus.vrf_cumulus import (
    _cumulus_get_vrf_api,
    _cumulus_get_vrf_netconf,
    _cumulus_get_vrf_ssh
)
from functions.vrf.extreme_vsp.vrf_extreme_vsp import (
    _extreme_vsp_get_vrf_api,
    _extreme_vsp_get_vrf_netconf,
    _extreme_vsp_get_vrf_ssh
)
from functions.vrf.ios.vrf_ios import (
    _ios_get_vrf_api,
    _ios_get_vrf_netconf,
    _ios_get_vrf_ssh
)
from functions.vrf.iosxr.vrf_iosxr import (
    _iosxr_get_vrf_api,
    _iosxr_get_vrf_netconf,
    _iosxr_get_vrf_ssh
)
from functions.vrf.juniper.vrf_juniper import (
    _juniper_get_vrf_api,
    _juniper_get_vrf_netconf,
    _juniper_get_vrf_ssh
)
from functions.vrf.napalm.vrf_napalm import (
    _generic_vrf_napalm
)
from functions.vrf.nxos.vrf_nxos import (
    _nxos_get_vrf_api,
    _nxos_get_vrf_netconf,
    _nxos_get_vrf_ssh
)
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
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: _juniper_get_vrf_api,
                self.SSH_CONNECTION: _juniper_get_vrf_ssh,
                self.NETCONF_CONNECTION: _juniper_get_vrf_netconf,
                self.NAPALM_CONNECTION: _generic_vrf_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: _cumulus_get_vrf_api,
                self.SSH_CONNECTION: _cumulus_get_vrf_ssh,
                self.NETCONF_CONNECTION: _cumulus_get_vrf_netconf,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: _arista_get_vrf_api,
                self.SSH_CONNECTION: _arista_get_vrf_ssh,
                self.NETCONF_CONNECTION: _arista_get_vrf_netconf,
                self.NAPALM_CONNECTION: _generic_vrf_napalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: _nxos_get_vrf_api,
                self.SSH_CONNECTION: _nxos_get_vrf_ssh,
                self.NETCONF_CONNECTION: _nxos_get_vrf_netconf,
                self.NAPALM_CONNECTION: _generic_vrf_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: _ios_get_vrf_api,
                self.SSH_CONNECTION: _ios_get_vrf_ssh,
                self.NETCONF_CONNECTION: _ios_get_vrf_netconf,
                self.NAPALM_CONNECTION: _generic_vrf_napalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: _iosxr_get_vrf_api,
                self.SSH_CONNECTION: _iosxr_get_vrf_ssh,
                self.NETCONF_CONNECTION: _iosxr_get_vrf_netconf,
                self.NAPALM_CONNECTION: _generic_vrf_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: _extreme_vsp_get_vrf_api,
                self.SSH_CONNECTION: _extreme_vsp_get_vrf_ssh,
                self.NETCONF_CONNECTION: _extreme_vsp_get_vrf_netconf,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
