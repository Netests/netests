#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.l2vni.l2vni_get import get_l2vni
from functions.l2vni.l2vni_compare import compare_l2vni
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    L2VNI_SRC_FILENAME,
    TEST_TO_EXC_L2VNI_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [l2vni_run.py]"
HEADER = "[l2vni_run.py]"


# #############################################################################
#
# Functions
#
def run_l2vni(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_L2VNI_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_L2VNI_KEY, False):
            get_l2vni(nr)
            same = compare_l2vni(
                nr=nr,
                l2vni_yaml_data=open_file(
                    f"{PATH_TO_VERITY_FILES}{L2VNI_SRC_FILENAME}"
                ),
            )
            if (
                test_to_execute[TEST_TO_EXC_L2VNI_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} L2VNI defined in"
                f"{PATH_TO_VERITY_FILES}{L2VNI_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} L2VNI have not been executed !!")
    else:
        print(
            f"{HEADER} L2VNI key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )

    return exit_value
