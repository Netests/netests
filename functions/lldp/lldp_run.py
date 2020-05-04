#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from functions.discovery_protocols.lldp.get_lldp import get_lldp
from functions.discovery_protocols.lldp.lldp_compare import compare_lldp
from functions.global_tools import open_file
from const.constants import (
    NOT_SET,
    LEVEL1,
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    LLDP_SRC_FILENAME,
    TEST_TO_EXC_LLDP_KEY,
)
from functions.verbose_mode import verbose_mode


ERROR_HEADER = "Error import [lldp_run.py]"
HEADER = "[lldp_run.py]"


def run_lldp(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_LLDP_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_LLDP_KEY] is True:
            get_lldp(nr)
            lldp_data = open_file(
                f"{PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME}"
            )
            same = compare_lldp(nr, lldp_data)
            if (
                test_to_execute[TEST_TO_EXC_LLDP_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} LLDP sessions are the same that defined in"
                f"{PATH_TO_VERITY_FILES}{LLDP_SRC_FILENAME} = {same} !!"
            )
        else:
            print(f"{HEADER} LLDP sessions tests are not executed !!")
    else:
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL1
        ):
            print(
                f"{HEADER} LLDP sessions key is not defined in"
                f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
            )

    return exit_value
