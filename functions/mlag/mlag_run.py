#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.mlag.mlag_get import get_mlag
from functions.mlag.mlag_compare import compare_mlag
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    MLAG_SRC_FILENAME,
    TEST_TO_EXC_MLAG_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [mlag_run.py]"
HEADER = "[mlag_run.py]"


# #############################################################################
#
# Functions
#
def run_mlag(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_MLAG_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_MLAG_KEY, False):
            get_mlag(nr)
            same = compare_mlag(
                nr=nr,
                mlag_yaml_data=open_file(
                    f"{PATH_TO_VERITY_FILES}{MLAG_SRC_FILENAME}"
                ),
            )
            if (
                test_to_execute.get(TEST_TO_EXC_MLAG_KEY) and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} MLAG defined in"
                f"{PATH_TO_VERITY_FILES}{MLAG_SRC_FILENAME} work = {same}!!"
            )
        else:
            print(f"{HEADER} MLAG have not been executed !!")
    else:
        print(
            f"{HEADER} MLAG key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
