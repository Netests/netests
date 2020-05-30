#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from netests import log
from netests.tools.file import open_file


def select_host_vars(hostname: str, groups: list, protocol: str):
    if truth_vars_exists() is False:
        log("Truth_vars doesn't exists")
        return {}

    if host_vars_exists(hostname, protocol):
        log.debug("Select hosts variables")
        return open_file(
            path=f"truth_vars/hosts/{hostname}/{protocol}.yml"
        )

    if group_vars_exists(groups[0], protocol):
        log.debug("Select groups variables")
        return open_file(
            path=f"truth_vars/groups/{groups[0]}/{protocol}.yml"
        )

    if all_vars_exists(protocol):
        log.debug("Select all variables")
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
