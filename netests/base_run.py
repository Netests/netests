#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from nornir.core import Nornir
from netests.base_protocols import MAPPING_PROTOCOLS

HEADER = "[netests - base_run.py]"


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

    if (
        parameters.get('test', False) is True or
        str(parameters.get('test', False)).upper() == "INFO"
    ):
        print_task_output = not init_data

        log.debug(
            f"\nExecute {MAPPING_PROTOCOLS.get(protocol).get('class')}"
            f"filename={MAPPING_PROTOCOLS.get(protocol).get('filename')}"
            f"key_store={MAPPING_PROTOCOLS.get(protocol).get('key_store')}"
            f"print_task_output={print_task_output}"
        )
        getter = MAPPING_PROTOCOLS.get(protocol).get('class')(
            nr=nr,
            options=parameters.get('options', {}),
            from_cli=False,
            num_workers=num_workers,
            verbose=verbose,
            print_task_output=print_task_output,
            protocol=protocol,
            filename=MAPPING_PROTOCOLS.get(protocol).get('filename'),
            key_store=MAPPING_PROTOCOLS.get(protocol).get('key_store')
        )
        getter.run()

        if (
            init_data and
            (
                protocol.upper() != "PING" or
                protocol.upper() != "BGP_UP"

            )
        ):
            getter.init_data()
            return True
        elif compare_data:
            getter.compare()
            return getter.get_compare_result()
        else:
            return True
