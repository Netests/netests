#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.socket.execute_socket import execute_socket
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    SOCKET_SRC_FILENAME,
    TEST_TO_EXC_SOCKET_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [socket_run.py]"
HEADER = "[socket_run.py]"


# #############################################################################
#
# Functions
#
def run_socket(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_SOCKET_KEY in test_to_execute.keys():
        if test_to_execute.get(TEST_TO_EXC_SOCKET_KEY, False):
            same = execute_socket(nr)
            if (
                test_to_execute[TEST_TO_EXC_SOCKET_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} Sockets defined in"
                f"{PATH_TO_VERITY_FILES}{SOCKET_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} Sockets have not been executed !!")
    else:
        print(
            f"{HEADER} SOCKET key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )

    return exit_value
