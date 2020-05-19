#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.getters.routing_get import GetterRouting
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
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: "pass",
                self.SSH_CONNECTION: "pass",
                self.NETCONF_CONNECTION: "pass",
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
