#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log


def log_compare(verity, host_data, hostname, groups):
    log.debug(
        "\n"
        f"COMPARE RESTULT for {hostname} / groups={groups}\n"
        "----------------------------\n"
        "Object from YAML file :\n"
        f"{verity}"
        "----------------------------\n"
        "Object from Running configuration :\n"
        f"{host_data}"
        "----------------------------\n"
    )
