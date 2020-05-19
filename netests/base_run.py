#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.getters.bgp_get import GetterBGP
from functions.getters.vrf_get import GetterVRF
from nornir.core import Nornir
from functions.global_tools import printline
from functions.base_init_data import create_truth_vars
from const.constants import (
    BGP_SRC_FILENAME,
    BOND_SRC_FILENAME,
    CDP_SRC_FILENAME,
    LLDP_SRC_FILENAME,
    FACTS_SRC_FILENAME,
    IPV4_SRC_FILENAME,
    IPV6_SRC_FILENAME,
    L2VNI_SRC_FILENAME,
    MLAG_SRC_FILENAME,
    MTU_SRC_FILENAME,
    OSPF_SRC_FILENAME,
    PING_SRC_FILENAME,
    SOCKET_SRC_FILENAME,
    STATIC_SRC_FILENAME,
    VLAN_SRC_FILENAME,
    VRF_SRC_FILENAME
)

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
