#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.bond.bond_get import get_bond
from functions.bond.bond_compare import compare_bond
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    BOND_SRC_FILENAME,
    TEST_TO_EXC_BOND_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [bond_run.py]"
HEADER = "[bond_run.py]"


# #############################################################################
#
# Functions
#
def run_bond(nr: Nornir, test_to_execute: dict):
    exit_value = True
    if TEST_TO_EXC_BOND_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_BOND_KEY].get("test"):
            get_bond(
                nr=nr,
                filters=test_to_execute.get(TEST_TO_EXC_BOND_KEY).get(
                    "filters", dict({})
                ),
            )
            bond_yaml_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{BOND_SRC_FILENAME}"
            )
            same = compare_bond(nr=nr, bond_yaml_data=bond_yaml_data)
            if (
                test_to_execute[TEST_TO_EXC_BOND_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} BOND defined in"
                f"{PATH_TO_VERITY_FILES}{BOND_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} BOND have not been executed !!")
    else:
        print(
            f"{HEADER} BOND key not found in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )

    return exit_value
