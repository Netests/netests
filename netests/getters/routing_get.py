#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        compare_data
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output,
            compare_data
        )

    def get_vrf(self):
        vrf = GetterVRF(
            nr=self.nr,
            options={},
            from_cli=False,
            num_workers=self.num_workers,
            verbose=self.verbose,
            print_task_output=False,
            compare_data=False
        ).run()
