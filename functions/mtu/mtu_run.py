#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.mtu.mtu_get import get_mtu
from functions.mtu.mtu_compare import compare_mtu
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    MTU_SRC_FILENAME,
    TEST_TO_EXC_MTU_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [mtu_run.py]"
HEADER = "[mtu_run.py]"


# #############################################################################
#
# Functions
#
def run_mtu(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_MTU_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_MTU_KEY, False):
            get_mtu(nr)
            same = compare_mtu(
                nr=nr, mtu_data=open_file(
                    f"{PATH_TO_VERITY_FILES}{MTU_SRC_FILENAME}"
                )
            )

            if (
                test_to_execute.get(TEST_TO_EXC_MTU_KEY) and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} MTU interfaces defined in"
                f"{PATH_TO_VERITY_FILES}{MTU_SRC_FILENAME} work = {same}!!"
            )
        else:
            print(f"{HEADER} MTU interfaces have not been executed !!")
    else:
        print(
            f"{HEADER} MTU interfaces key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
