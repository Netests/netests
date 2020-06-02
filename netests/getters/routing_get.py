#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import VRF_DATA_KEY
from netests.getters.vrf_get import GetterVRF
from netests.getters.base_get import GetterBase


class GetterRouting(GetterBase):

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

    def run(self):
        self.get_vrf()
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def get_vrf(self):
        GetterVRF(
            nr=self.nr,
            options={},
            from_cli=False,
            num_workers=self.num_workers,
            verbose=self.verbose,
            print_task_output=False,
            filename="vrf.yml",
            protocol="vrf",
            key_store=VRF_DATA_KEY,
        ).run()
