#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-


from nornir.core import Nornir
from functions.bgp.bgp_compare import compare_bgp
from functions.bgp.bgp_checks import get_bgp_up
from functions.bgp.bgp_reports import create_reports
from functions.bgp.bgp_gets import get_bgp
from functions.global_tools import open_file
from const.constants import (
    PATH_TO_VERITY_FILES,
    TEST_TO_EXECUTE_FILENAME,
    BGP_SRC_FILENAME,
    TEST_TO_EXC_BGP_KEY,
    TEST_TO_EXC_BGP_UP_KEY,
)


ERROR_HEADER = "Error import [bgp_run.py]"
HEADER = "[bgp_run.py]"


def run_bgp(nr: Nornir, test_to_execute: dict, *, reports=False) -> bool:

    exit_value = True

    if test_to_execute.get(TEST_TO_EXC_BGP_KEY, False):
        get_bgp(nr)
        bgp_data = open_file(
            f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"
        )
        same = compare_bgp(nr, bgp_data)
        if reports:
            create_reports(nr, bgp_data)
        if (
            test_to_execute[TEST_TO_EXC_BGP_KEY] and
            same is False
        ):
            exit_value = False
        print(
            f"{HEADER} BGP sessions are the same that defined in"
            f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME} = {same} !!"
        )
    else:
        print(
            f"{HEADER} BGP key not found in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )
    return exit_value


def run_bgp_up(nr: Nornir, test_to_execute: dict) -> bool:
    exit_value = True
    if test_to_execute[TEST_TO_EXC_BGP_UP_KEY] is True:
        works = get_bgp_up(nr)
        bgp_data = open_file(
            f"{PATH_TO_VERITY_FILES}{BGP_SRC_FILENAME}"
        )
        print(bgp_data)
        if (
            test_to_execute[TEST_TO_EXC_BGP_UP_KEY] and
            works is False
        ):
            exit_value = False

        print(f"{HEADER} All BGP sessions on devices are UP = {works} !!")
    else:
        print(
            f"{HEADER} BGP_UP key not found in"
            f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}  !!"
        )
    return exit_value
