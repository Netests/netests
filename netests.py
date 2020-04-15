#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import urllib3
from functions.base_run import run_base
from functions.base_cli import netests_cli
from functions.global_tools import (
    printline_comment_json as p,
    open_file,
    check_devices_connectivity,
)
from functions.nornir_inventory import init_nornir
from const.constants import (
    NETESTS_CONFIG,
    PATH_TO_INVENTORY_FILES,
    ANSIBLE_INVENTORY,
    EXIT_FAILURE,
    EXIT_SUCCESS,
)


HEADER = "[netests - main.py]"


@click.command()
@click.version_option(version="© Dylan Hamel v0.0.1")
@click.option(
    "-a",
    "--netest-config-file",
    default="netests.yml",
    show_default=True,
    help="Path to Netests configuration file"
)
@click.option(
    "-b",
    "--inventory-config-file",
    default=False,
    show_default=True,
    help="Specify path to a Nonrnir configuration file."
)
@click.option(
    "-c",
    "--check-connectivity",
    default=False,
    show_default=True,
    help="Check if devices are reachable",
)
@click.option(
    "-d",
    "--devices",
    default="#",
    show_default=True,
    help="Filter devices based on the hostname."
            'Several hostname can be given separate by a ","',
)
@click.option(
    "-e",
    "--devices-number",
    default=-1,
    show_default=True,
    help="Define how many devices will be selected from the inventory."
            "Can be combined with --device-group",
)
@click.option(
    "-g",
    "--devices-group",
    default="#",
    show_default=True,
    help="Filter devices based on the group."
            "Allow you to select device only from a group."
            'Several groups can be given separate by a ","',
)
@click.option(
    "-i",
    "--inventory",
    default="inventory.yml",
    show_default=True,
    help="Path to Ansible inventory or Nornir hosts.yml",
)
@click.option(
    "-j",
    "--nornir-groups-file",
    default="groups.yml",
    show_default=True,
    help="Path to Nornir groups.yml",
)
@click.option(
    "-k",
    "--nornir-defaults-file",
    default="defaults.yml",
    show_default=True,
    help="Path to Nornir defaults.yml",
)
@click.option(
    "-l",
    "--netbox-url",
    default="https://127.0.0.1",
    show_default=True,
    help="Netbox URL",
)
@click.option(
    "-m",
    "--netbox-token",
    default="abcdefghijklmnopqrstuvwxyz0123456789",
    show_default=True,
    help="Netbox Token",
)

@click.option(
    "-n",
    "--netbox-ssl",
    default=True,
    show_default=True,
    help="Verify the Netbox certificate",
)
@click.option(
    "-r",
    "--reports",
    default=False,
    show_default=True,
    help="If set a configuration reports will be create",
)
@click.option(
    "-t",
    "--terminal",
    default=False,
    show_default=True,
    help="Start the terminal Netests application"
)
@click.option(
    "-v",
    "--verbose",
    default="level0",
    show_default=True,
    help="Filter devices based on the hostname."
            'Several hostname can be given separate by a ","',
)
@click.option(
    "-w",
    "--num-workers",
    default=100,
    show_default=True,
    help="Define the number of parallel jobs.",
)
@click.option(
    "-x",
    "--ansible-inventory",
    default=False,
    show_default=True,
    help="Specify that an Ansible inventory will be used.",
)
@click.option(
    "-y",
    "--netbox-inventory",
    default=False,
    show_default=True,
    help="Specify that an Netbox inventory will be used.",
)
@click.option(
    "-z",
    "--nornir-inventory",
    default=False,
    show_default=True,
    help="Specify that an Nornir inventory will be used.",
)
def main(
    netest_config_file,
    inventory_config_file,
    check_connectivity,
    devices,
    devices_number,
    devices_group,
    inventory,
    nornir_groups_file,
    nornir_defaults_file,
    netbox_url,
    netbox_token,
    netbox_ssl,
    reports,
    terminal,
    verbose,
    num_workers,
    ansible_inventory,
    netbox_inventory,
    nornir_inventory
):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if terminal:
        netests_cli(ansible, virtual, netbox)
        exit(EXIT_SUCCESS)

    t = open_file(path=netest_config_file)

    os.environ["NETESTS_VERBOSE"] = f"{verbose}"

    # Create Nornir object
    try:
        nr = init_nornir(
            log_file="./nornir/nornir.log",
            log_level="debug",
            ansible_inventory=ansible_inventory,
            nornir_inventory=nornir_inventory,
            netbox_inventory=netbox_inventory,
            num_workers=num_workers,
            inventory_config_file=inventory_config_file,
            inventory=inventory,
            nornir_groups_file=nornir_groups_file,
            nornir_defaults_file=nornir_defaults_file,
            netbox_url=netbox_url,
            netbox_token=netbox_token,
            netbox_ssl=netbox_ssl,
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

    exit_value = True
    for k, v in t.get('config').get('protocols').items():
        if (
            run_base(nr=nr, protocol=k, parameters=v) is False and
            exit_value is True
        ):
            exit_value = False

    return exit_value


if __name__ == "__main__":
    main()
