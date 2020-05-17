#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.getters.routing_get import GetterRouting
from functions.bgp.juniper.bgp_juniper import (
    _juniper_get_bgp_ssh,
    _juniper_get_bgp_api,
    _juniper_get_bgp_netconf
)
from functions.bgp.cumulus.bgp_cumulus import (
    _cumulus_get_bgp_ssh,
    _cumulus_get_bgp_api,
    _cumulus_get_bgp_netconf
)
from functions.bgp.arista.bgp_arista import (
    _arista_get_bgp_ssh,
    _arista_get_bgp_api,
    _arista_get_bgp_netconf
)
from functions.bgp.nxos.bgp_nxos import (
    _nexus_get_bgp_ssh,
    _nexus_get_bgp_api,
    _nexus_get_bgp_netconf
)
from functions.bgp.ios.bgp_ios import (
    _ios_get_bgp_ssh,
    _ios_get_bgp_api,
    _ios_get_bgp_netconf
)
from functions.bgp.iosxr.bgp_iosxr import (
    _iosxr_get_bgp_ssh,
    _iosxr_get_bgp_api,
    _iosxr_get_bgp_netconf
)
from functions.bgp.extreme_vsp.bgp_extreme_vsp import (
    _extreme_vsp_get_bgp_ssh,
    _extreme_vsp_get_bgp_api,
    _extreme_vsp_get_bgp_netconf
)
from functions.bgp.napalm.bgp_napalm import (
    _generic_bgp_napalm
)
from const.constants import BGP_SESSIONS_HOST_KEY


HEADER = "[netests - get_bgp]"


class GetterBGP(GetterRouting):

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

    def run(self):
        self.get_vrf()
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def print_result(self):
        self.print_protocols_result(BGP_SESSIONS_HOST_KEY, "BGP")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: _juniper_get_bgp_api,
                self.SSH_CONNECTION: _juniper_get_bgp_ssh,
                self.NETCONF_CONNECTION: _juniper_get_bgp_netconf,
                self.NAPALM_CONNECTION: _generic_bgp_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: _cumulus_get_bgp_api,
                self.SSH_CONNECTION: _cumulus_get_bgp_ssh,
                self.NETCONF_CONNECTION: _cumulus_get_bgp_netconf,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: _arista_get_bgp_api,
                self.SSH_CONNECTION: _arista_get_bgp_ssh,
                self.NETCONF_CONNECTION: _arista_get_bgp_netconf,
                self.NAPALM_CONNECTION: _generic_bgp_napalm
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: _nexus_get_bgp_api,
                self.SSH_CONNECTION: _nexus_get_bgp_ssh,
                self.NETCONF_CONNECTION: _nexus_get_bgp_netconf,
                self.NAPALM_CONNECTION: _generic_bgp_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: _ios_get_bgp_api,
                self.SSH_CONNECTION: _ios_get_bgp_ssh,
                self.NETCONF_CONNECTION: _ios_get_bgp_netconf,
                self.NAPALM_CONNECTION: _generic_bgp_napalm
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: _iosxr_get_bgp_api,
                self.SSH_CONNECTION: _iosxr_get_bgp_ssh,
                self.NETCONF_CONNECTION: _iosxr_get_bgp_netconf,
                self.NAPALM_CONNECTION: _generic_bgp_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: _extreme_vsp_get_bgp_api,
                self.SSH_CONNECTION: _extreme_vsp_get_bgp_ssh,
                self.NETCONF_CONNECTION: _extreme_vsp_get_bgp_netconf,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
