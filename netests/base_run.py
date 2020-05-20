#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core import Nornir
from netests.getters.bgp_get import GetterBGP
from netests.getters.vrf_get import GetterVRF
from netests.base_init_data import create_truth_vars

HEADER = "[netests - base_run.py]"
RUN = {
    "bgp": GetterBGP,
    "vrf": GetterVRF
}


def run_base(
    nr: Nornir,
    protocol: str,
    not_compare: bool,
    parameters: dict,
    init_data: bool,
    num_workers: int,
    verbose: str
) -> bool:
    if (
        parameters.get('test', False) is True or
        str(parameters.get('test', False)).upper() == "INFO"
    ):
        result_output = list()
        getter = RUN.get(protocol)(
            nr=nr,
            options=parameters.get('options', {}),
            from_cli=False,
            num_workers=num_workers,
            verbose=verbose,
            print_task_output=True
        )

        getter.run()

        """
        if init_data is True:
            if protocol != "ping":
                create_truth_vars(
                    nr=nr,
                    protocol=protocol
                )
        elif not_compare is False:
            same = RUN.get(protocol).get('compare')(
                nr=nr,
                options=parameters.get('options', {})
            )
            result_output.append(f"{HEADER}({protocol}) is working = {same}")
        
        printline()
        print("\n".join(result_output))

        return (
            parameters.get('test', False) is True and
            same is False
        )
        """

    else:
        return True
