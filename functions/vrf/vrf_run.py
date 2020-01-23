#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.vrf.vrf_get import get_vrf
from functions.vrf.vrf_compare import compare_vrf
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    VRF_SRC_FILENAME,
    TEST_TO_EXC_VRF_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [vrf_run.py]"
HEADER = "[vrf_run.py]"


# #############################################################################
#
# Functions
#
def run_vrf(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_VRF_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_VRF_KEY, False):
            get_vrf(nr)
            vrf_data = open_file(
                f"{PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME}"
            )
            same = compare_vrf(nr, vrf_data)
            if (
                test_to_execute[TEST_TO_EXC_VRF_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} VRF are the same that defined in"
                f"{PATH_TO_VERITY_FILES}{VRF_SRC_FILENAME} = {same} !!"
            )
        else:
            print(f"{HEADER} VRF tests are not executed !!")
    else:
        print(
            f"{HEADER} VRF key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
