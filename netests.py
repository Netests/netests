#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.base_run import run_base
from functions.global_tools import (
    printline_comment_json as p,
    open_file,
    init_nornir,
    check_devices_connectivity,
)
from const.constants import (
    PATH_TO_INVENTORY_FILES,
    ANSIBLE_INVENTORY,
    PATH_TO_VERITY_FILES,
    TEST_TO_EXECUTE_FILENAME,
    EXIT_FAILURE,
    EXIT_SUCCESS,
)
import urllib3
import click


ERROR_HEADER = "Error import [main.py]"
HEADER = "[netests - main.py]"


@click.command()
@click.version_option(version="© Dylan Hamel v0.0.1")
@click.option(
    "-a",
    "--ansible",
    default=f"{PATH_TO_INVENTORY_FILES}{ANSIBLE_INVENTORY}",
    show_default=True,
    help=f"Define path to the production Ansible inventory file",
)
@click.option(
    "-o",
    "--virtual",
    default=False,
    show_default=True,
    help=f"Define path to the virtual Ansible inventory file",
)
@click.option(
    "-n",
    "--netbox",
    default=False,
    show_default=True,
    help=f"Define path to retrieve inventory from netbox (in progress)",
)
@click.option(
    "-r",
    "--reports",
    default=False,
    show_default=True,
    help=f"If TRUE, configuration reports will be create",
)
@click.option(
    "-c",
    "--check-connectivity",
    default=False,
    show_default=True,
    help=f"If TRUE, check if devices are reachable",
)
@click.option(
    "-s",
    "--devices-number",
    default=-1,
    show_default=True,
    help=f"Define how many devices will be selected from the inventory."
    f"Can be combined with --device-group",
)
@click.option(
    "-g",
    "--devices-group",
    default="#",
    show_default=True,
    help=f"Filter devices based on the group."
    f"Allow you to select device only from a group."
    f'Several groups can be given separate by a ","',
)
@click.option(
    "-d",
    "--devices",
    default="#",
    show_default=True,
    help=f"Filter devices based on the hostname."
    f'Several hostname can be given separate by a ","',
)
@click.option(
    "-v",
    "--verbose",
    default="level0",
    show_default=True,
    help=f"Filter devices based on the hostname."
    f'Several hostname can be given separate by a ","',
)
def main(
    ansible,
    virtual,
    netbox,
    reports,
    check_connectivity,
    devices_number,
    devices_group,
    devices,
    verbose
):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    os.environ["NETESTS_VERBOSE"] = f"{verbose}"

    print(ansible, netbox)
    # Create Nornir object
    try:
        nr = init_nornir(
            log_file="./nornir/nornir.log",
            log_level="debug",
            ansible=ansible,
            virtual=virtual,
            netbox=netbox,
        )
    except FileNotFoundError as e:
        print(f"{HEADER} Inventory file not found ...")
        print(f"{HEADER} {e}")
        exit(EXIT_FAILURE)

    p(comment="Devices selected", json_to_print=nr.inventory.hosts)

    if check_connectivity:
        if check_devices_connectivity(nr):
            exit(EXIT_SUCCESS)
        else:
            exit(EXIT_FAILURE)

    t = open_file(f"{PATH_TO_VERITY_FILES}{TEST_TO_EXECUTE_FILENAME}")
    exit_value = True

    for k, v in t.items():
        if (
            run_base(nr=nr, protocol=k, parameters=v) is False and
            exit_value is True
        ):
            exit_value = False

    return exit_value


if __name__ == "__main__":
    main()
