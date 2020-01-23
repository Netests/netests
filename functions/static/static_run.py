#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.static.static_get import get_static
from functions.static.static_compare import compare_static
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    STATIC_SRC_FILENAME,
    TEST_TO_EXC_STATIC_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [static_run.py]"
HEADER = "[static_run.py]"


# #############################################################################
#
# Functions
#
def run_static(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_STATIC_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get("test", False):
            get_static(nr)
            same = compare_static(
                nr=nr,
                ansible_vars=test_to_execute.get(TEST_TO_EXC_STATIC_KEY)
                .get("ansible_vars")
                .get("enable", False),
                dict_keys=test_to_execute.get(TEST_TO_EXC_STATIC_KEY)
                .get("ansible_vars")
                .get("dict_keys", False),
                your_keys=test_to_execute.get(TEST_TO_EXC_STATIC_KEY)
                .get("ansible_vars")
                .get("your_keys", False),
            )
            if (
                test_to_execute.get(TEST_TO_EXC_STATIC_KEY).get("test", False)
                and same is False
            ):
                exit_value = False
            print(
                f"{HEADER} Static routes defined in"
                f"{PATH_TO_VERITY_FILES}{STATIC_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} Static routes have not been executed !!")
    else:
        print(
            f"{HEADER} Static routes key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
