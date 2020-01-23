#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.ping.execute_ping import execute_ping
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    PING_SRC_FILENAME,
    TEST_TO_EXC_PING_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [ping_run.py]"
HEADER = "[ping_run.py]"


# #############################################################################
#
# Functions
#
def run_ping(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_PING_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_PING_KEY, False):
            works = execute_ping(nr)
            if (
                test_to_execute[TEST_TO_EXC_PING_KEY] and
                works is False
            ):
                exit_value = False
            print(
                f"{HEADER} Pings defined in"
                f"{PATH_TO_VERITY_FILES}{PING_SRC_FILENAME} work = {works} !!"
            )
        else:
            print(f"{HEADER} Pings have not been executed !!")
    else:
        print(
            f"{HEADER} PING key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
        )

    return exit_value
