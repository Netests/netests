#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.vlan.vlan_get import get_vlan
from functions.vlan.vlan_compare import compare_vlan
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    VLAN_SRC_FILENAME,
    TEST_TO_EXC_VLAN_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [vlan_run.py]"
HEADER = "[vlan_run.py]"


# #############################################################################
#
# Functions
#
def run_vlan(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_VLAN_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_VLAN_KEY).get("test", False):
            get_vlan(
                nr=nr,
                filters=test_to_execute.get(TEST_TO_EXC_VLAN_KEY).get(
                    "filters", dict({})
                ),
            )
            same = compare_vlan(
                nr=nr,
                vlan_yaml_data=open_file(
                    f"{PATH_TO_VERITY_FILES}{VLAN_SRC_FILENAME}"
                ),
            )
            if (
                test_to_execute[TEST_TO_EXC_VLAN_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} VLAN defined in"
                f"{PATH_TO_VERITY_FILES}{VLAN_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} VLAN have not been executed !!")
    else:
        print(
            f"{HEADER} VLAN key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )

    return exit_value
