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


def log_no_yaml_data(prot, key, key_string, hostname, groups):
    log.debug(
        "\n"
        f"COMPARE FUNCTION WAS NOT EXECUTED FOR PROTOCOL={prot} - {hostname}\n"
        f"This function is not executed for two potential reasons :\n"
        f" 1) No data found in a YAML file for host {hostname} / {groups}.\n"
        f"    Please be sure that data is defined for this host / protocol\n\n"
        f" 2) No data is stored with the key {key} - {key_string}.\n"
        f"    Please check netests.log file to check why no data is stored\n"
    )
