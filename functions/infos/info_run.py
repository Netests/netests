#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.infos.infos_get import get_infos
from functions.infos.infos_compare import compare_infos
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    INFOS_SRC_FILENAME,
    TEST_TO_EXC_INFOS_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [info_run.py]"
HEADER = "[info_run.py]"


# #############################################################################
#
# Functions
#
def run_info(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_INFOS_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_INFOS_KEY) is True:
            get_infos(nr)
            same = compare_infos(
                nr=nr,
                infos_data=open_file(
                    f"{PATH_TO_VERITY_FILES}{INFOS_SRC_FILENAME}"
                ),
            )
            if (
                test_to_execute.get(TEST_TO_EXC_INFOS_KEY) and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} System informations defined in"
                f"{PATH_TO_VERITY_FILES}{INFOS_SRC_FILENAME} work = {same}!!"
            )
        else:
            print(f"{HEADER} System informations have not been executed !!")
    else:
        print(
            f"{HEADER} System informations key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
