#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

# #############################################################################
#
# Import Library
#
from nornir.core import Nornir
from functions.ip.ipv6.ipv6_get import get_ipv6
from functions.ip.ipv6.ipv6_compare import compare_ipv6
from functions.global_tools import open_file
from const.constants import (
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    IPV6_SRC_FILENAME,
    TEST_TO_EXC_IPV6_KEY,
)

# #############################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [ipv6_run.py]"
HEADER = "[ipv6_run.py]"


# #############################################################################
#
# Functions
#
def run_ipv6(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_IPV6_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_IPV6_KEY].get("test"):
            get_ipv6(
                nr=nr,
                filters=test_to_execute.get(TEST_TO_EXC_IPV6_KEY).get(
                    "filters", dict({})
                ),
            )
            ipv6_yaml_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{IPV6_SRC_FILENAME}"
            )
            same = compare_ipv6(nr, ipv6_yaml_data)
            if (
                test_to_execute[TEST_TO_EXC_IPV6_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} IPv6 addresses defined in"
                f"{PATH_TO_VERITY_FILES}{IPV6_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} IPv6 addresses have not been executed !!")
    else:
        print(
            f"{HEADER} IPv6 addresses key is not defined in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )

    return exit_value
