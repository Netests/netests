#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from nornir.core import Nornir
from netests.getters.bgp_get import GetterBGP
from netests.getters.cdp_get import GetterCDP
from netests.getters.facts_get import GetterFacts
from netests.getters.lldp_get import GetterLLDP
from netests.getters.ospf_get import GetterOSPF
from netests.getters.vrf_get import GetterVRF
from netests.base_init_data import create_truth_vars

HEADER = "[netests - base_run.py]"
RUN = {
    "bgp": GetterBGP,
    "cdp": GetterCDP,
    "facts": GetterFacts,
    "lldp": GetterLLDP,
    "ospf": GetterOSPF,
    "vrf": GetterVRF
}


def run_base(
    nr: Nornir,
    protocol: str,
    compare_data: bool,
    parameters: dict,
    init_data: bool,
    num_workers: int,
    verbose: str
) -> bool:

    log.debug(
        "\n"
        f"protocol={protocol}\n"
        f"compare_data={compare_data}\n"
        f"parameters={parameters}\n"
        f"init_data={init_data}\n"
        f"num_workers={num_workers}\n"
        f"verbose={verbose}\n"
    )

    result = dict()
    if (
        parameters.get('test', False) is True or
        str(parameters.get('test', False)).upper() == "INFO"
    ):
        log.debug(f"Execute {RUN.get(protocol)}")
        result_output = list()
        getter = RUN.get(protocol)(
            nr=nr,
            options=parameters.get('options', {}),
            from_cli=False,
            num_workers=num_workers,
            verbose=verbose,
            print_task_output=True,
            compare_data=compare_data
        )

        getter.run()
        getter.compare()
        return getter.get_compare_result()
