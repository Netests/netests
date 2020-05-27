#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from netests.tools.file import open_file
from netests.constants import NOT_SET


HEADER = "[netests - select_vars.py] -"


def select_host_vars(hostname: str, groups: list, protocol: str):
    if truth_vars_exists() is False:
        #print(f"{HEADER} Truth_vars doesn't exists")
        return {}

    if host_vars_exists(hostname, protocol):
        #print(f"{HEADER} Select hosts variables")
        return open_file(
            path=f"truth_vars/hosts/{hostname}/{protocol}.yml"
        )

    if group_vars_exists(groups[0], protocol):
        #print(f"{HEADER} Select groups variables")
        return open_file(
            path=f"truth_vars/groups/{groups[0]}/{protocol}.yml"
        )

    if all_vars_exists(protocol):
        #print(f"{HEADER} Select all variables")
        return open_file(
            path=f"truth_vars/all/{protocol}.yml"
        )


def truth_vars_exists() -> bool:
    os.path.exists("truth_vars")


def host_vars_exists(hostname: str, protocol: str) -> bool:
    return (
        os.path.exists("truth_vars/hosts") and
        os.path.exists(f"truth_vars/hosts/{hostname}") and
        os.path.exists(f"truth_vars/hosts/{hostname}/{protocol}.yml")
    )


def group_vars_exists(group: str, protocol: str) -> bool:
    return os.path.exists(f"truth_vars/groups/{group}/{protocol}.yml")


def all_vars_exists(protocol: str) -> bool:
    return (
        os.path.exists("truth_vars/all") and
        os.path.exists(f"truth_vars/all/{protocol}.yml")
    )
