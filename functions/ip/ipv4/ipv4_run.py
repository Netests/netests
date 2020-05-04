#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from functions.ip.ipv4.ipv4_get import get_ipv4
from functions.ip.ipv4.ipv4_compare import compare_ipv4
from functions.global_tools import open_file
from const.constants import (
    NOT_SET,
    LEVEL1,
    TEST_TO_EXECUTE_FILENAME,
    PATH_TO_VERITY_FILES,
    IPV4_SRC_FILENAME,
    TEST_TO_EXC_IPV4_KEY,
)
from functions.verbose_mode import verbose_mode


ERROR_HEADER = "Error import [ipv4_run.py]"
HEADER = "[ipv4_run.py]"


def run_ipv4(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if TEST_TO_EXC_IPV4_KEY in test_to_execute.keys():
        if test_to_execute[TEST_TO_EXC_IPV4_KEY].get("test", False):
            get_ipv4(
                nr=nr,
                filters=test_to_execute.get(TEST_TO_EXC_IPV4_KEY).get(
                    "filters", dict({})
                ),
            )
            ipv4_yaml_data = open_file(
                path=f"{PATH_TO_VERITY_FILES}{IPV4_SRC_FILENAME}"
            )
            same = compare_ipv4(nr, ipv4_yaml_data)
            if (
                test_to_execute[TEST_TO_EXC_IPV4_KEY] and
                same is False
            ):
                exit_value = False
            print(
                f"{HEADER} IPv4 addresses defined in"
                f"{PATH_TO_VERITY_FILES}{IPV4_SRC_FILENAME} work = {same} !!"
            )
        else:
            print(f"{HEADER} IPv4 addresses have not been executed !!")
    else:
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL1
        ):
            print(
                f"{HEADER} IPv4 addresses key is not defined in"
                f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME} !!"
            )

    return exit_value
