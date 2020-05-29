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
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
)


HEADER = "[netests - base_run.py]"
RUN = {
    "bgp": {
        "class": GetterBGP,
        "filename": "bgp.yml",
        "key_store": BGP_SESSIONS_HOST_KEY
    },
    "cdp": {
        "class": GetterCDP,
        "filename": "cdp.yml",
        "key_store": CDP_DATA_HOST_KEY
    },
    "facts": {
        "class": GetterFacts,
        "filename": "facts.yml",
        "key_store": FACTS_DATA_HOST_KEY
    },
    "lldp": {
        "class": GetterLLDP,
        "filename": "lldp.yml",
        "key_store": LLDP_DATA_HOST_KEY
    },
    "ospf": {
        "class": GetterOSPF,
        "filename": "ospf.yml",
        "key_store": OSPF_SESSIONS_HOST_KEY
    },
    "vrf": {
        "class": GetterVRF,
        "filename": "vrf.yml",
        "key_store": VRF_DATA_KEY
    },
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
        print_task_output = not init_data

        log.debug(
            f"\nExecute {RUN.get(protocol).get('class')}"
            f"filename={RUN.get(protocol).get('filename')}"
            f"key_store={RUN.get(protocol).get('key_store')}"
            f"print_task_output={print_task_output}"
        )
        result_output = list()
        getter = RUN.get(protocol).get('class')(
            nr=nr,
            options=parameters.get('options', {}),
            from_cli=False,
            num_workers=num_workers,
            verbose=verbose,
            print_task_output=print_task_output,
            protocol=protocol,
            filename=RUN.get(protocol).get('filename'),
            key_store=RUN.get(protocol).get('key_store')
        )
        getter.run()

        if init_data:
            getter.init_data()
            return True
        elif compare_data:
            getter.compare()
            return getter.get_compare_result()
        else:
            return True
