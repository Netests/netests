#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.discovery_protocols.cdp.get_cdp import get_cdp
from functions.discovery_protocols.cdp.cdp_compare import compare_cdp
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    CDP_SRC_FILENAME,
    TEST_TO_EXC_CDP_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [cdp_run.py]"
HEADER = "[cdp_run.py]"


# #############################################################################
#
# Functions
#
def run_cdp(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_CDP_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_CDP_KEY] is True:
            get_cdp(nr)
            cdp_data = open_file(
                f"{PATH_TO_VERITY_FILES}{CDP_SRC_FILENAME}"
            )
            same = compare_cdp(nr, cdp_data)
            if (
                test_to_execute[TEST_TO_EXC_CDP_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} CDP sessions are the same that defined in"
                f"{PATH_TO_VERITY_FILES}{CDP_SRC_FILENAME} = {same} !!"
            )
        else:
            print(f"{HEADER} CDP sessions tests are not executed !!")
    else:
        print(
            f"{HEADER} CDP sessions key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )
    return exit_value