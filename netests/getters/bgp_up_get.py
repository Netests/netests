#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from netests.getters.bgp_get import GetterBGP
from netests.comparators.bgp_up_compare import _compare_transit_bgp_up


class GetterBGPUp(GetterBGP):

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

    def compare(self):
        log.debug(
            f"CALL _compare_transit_bgp_up  num_workers={self.num_workers}"
        )
        data = self.devices.run(
            task=_compare_transit_bgp_up,
            on_failed=True,
            num_workers=self.num_workers
        )
        self._compare_result(data)
