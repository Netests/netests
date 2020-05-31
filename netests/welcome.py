#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import shutil
import urllib3
from netests import log
from netests.base_run import run_base
from netests.base_cli import netests_cli
from netests.select_vars import select_host_vars
from netests.nornir_inventory import init_nornir
from netests.tools.std import open_file, check_devices_connectivity
from netests.constants import EXIT_FAILURE, EXIT_SUCCESS, DATA_MODELS_PATH
import pprint
PP = pprint.PrettyPrinter(indent=4)


HEADER = "[netests - main.py]"


def print_banner(nr, content_file):
    printline()
    print_hello()
    printline()
    print_inv(nr)
    printline()
    print_protocols(content_file)


def print_protocols(content_file):
    pdict = dict()
    for k, v in content_file.get('config').get('protocols').items():
        pdict[k] = v.get('test', False)
    PP.pprint(pdict)


def print_inv(nr):
    to_print = dict()
    for host in nr.inventory.hosts:
        to_print[host] = dict()
        to_print[host]['hostname'] = nr.inventory.hosts[host].hostname
        to_print[host]['connexion'] = nr.inventory.hosts[host]['connexion']
        to_print[host]['port'] = nr.inventory.hosts[host].port
        to_print[host]['platform'] = nr.inventory.hosts[host].platform
    PP.pprint(to_print)


def print_hello() -> None:
    print("\t Welcome to Netests.io ")


def printline() -> None:
    size = int(shutil.get_terminal_size()[0] / 2)
    print("*-" * size)


def print_result(result) -> None:
    PP.pprint(result)


@click.command()
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
    is_flag=True,
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
    is_flag=True,
    help="If set a configuration reports will be create",
)
@click.option(
    "-t",
    "--terminal",
    is_flag=True,
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
    is_flag=True,
    help="Specify that an Ansible inventory will be used.",
)
@click.option(
    "-y",
    "--netbox-inventory",
    is_flag=True,
    help="Specify that an Netbox inventory will be used.",
)
@click.option(
    "-z",
    "--nornir-inventory",
    is_flag=True,
    help="Specify that an Nornir inventory will be used.",
)
@click.option(
    "-C",
    "--compare",
    default=True,
    help="To compare/excute step. Will only get data or generate cmd.",
)
@click.option(
    "-D",
    "--show-data-model",
    default=False,
    help="Show data models for a protocol. Can help you to create your SOT.",
)
@click.option(
    "-I",
    "--init-data",
    is_flag=True,
    help="To create truth_vars files.",
)
@click.option(
    "-V",
    "--show-truth-vars",
    default=False,
    help="Show vars retrieved for a specific host. Use * to select all hosts",
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
    nornir_inventory,
    compare,
    show_data_model,
    init_data,
    show_truth_vars
):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    if show_data_model is not False:
        if os.path.exists(f"{DATA_MODELS_PATH}{show_data_model}.yml"):
            with open(f"{DATA_MODELS_PATH}{show_data_model}.yml", 'r') as f:
                print(f.read())
        else:
            print(f"{HEADER} {show_data_model} is not a supported protocol")
        exit(EXIT_SUCCESS)

    t = open_file(path=netest_config_file)
    log.debug(t)

    # Create Nornir object
    try:
        nr = init_nornir(
            log_file="./netests.log",
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

    if terminal:
        netests_cli(nr)
        exit(EXIT_SUCCESS)

    print_banner(nr, t)

    if check_connectivity:
        if check_devices_connectivity(nr):
            exit(EXIT_SUCCESS)
        else:
            exit(EXIT_FAILURE)
    elif show_truth_vars is not False:
        result = dict()
        result['error_not_in_inventory'] = list()
        for hostname in show_truth_vars.split(','):
            if hostname in nr.inventory.hosts.keys():
                result[hostname] = dict()
                for protocol, test in t.get('config').get('protocols').items():
                    if test.get('test', False) is True:
                        result[hostname][protocol] = select_host_vars(
                            hostname=hostname,
                            groups=nr.inventory.hosts[hostname].groups,
                            protocol=protocol
                        )

            else:
                result['error_not_in_inventory'].append(hostname)

        printline()
        PP.pprint(result)
        exit(EXIT_SUCCESS)

    result = dict()
    for k, v in t.get('config').get('protocols').items():
        result[k] = run_base(
            nr=nr,
            protocol=k,
            compare_data=compare,
            parameters=v,
            init_data=init_data,
            num_workers=num_workers,
            verbose=verbose
        )

    if init_data is False:
        printline()
        print_result(result)


if __name__ == "__main__":
    main()
