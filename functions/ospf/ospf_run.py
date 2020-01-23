#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.ospf.ospf_gets import get_ospf
from functions.ospf.ospf_compare import compare_ospf
from functions.global_tools import open_file, get_level_test
from const.constants import (
    NOT_SET,
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    OSPF_SRC_FILENAME,
    TEST_TO_EXC_OSPF_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [ospf_run.py]"
HEADER = "[ospf_run.py]"


# #############################################################################
#
# Functions
#
def run_ospf(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_OSPF_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_OSPF_KEY].get("test", False):
            get_ospf(nr)
            ospf_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{OSPF_SRC_FILENAME}"
            )
            works = compare_ospf(
                nr=nr,
                ospf_data=ospf_data,
                level_test=get_level_test(
                    level_value=test_to_execute.get(TEST_TO_EXC_OSPF_KEY).get(
                        "level", NOT_SET
                    )
                ),
            )
            if (
                test_to_execute[TEST_TO_EXC_OSPF_KEY] and
                works is False
            ):
                exit_value = False
            print(
                f"{HEADER} OSPF sessions defined in"
                f"{PATH_TO_VERITY_FILES}{OSPF_SRC_FILENAME} work = {works} !!"
            )
        else:
            print(f"{HEADER} OSPF have not been executed !!")
    else:
        print(
            f"{HEADER} OSPF sessions  key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
