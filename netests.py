#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.bgp.bgp_run import run_bgp, run_bgp_up
from functions.bond.bond_run import run_bond
from functions.discovery_protocols.lldp.lldp_run import run_lldp
from functions.discovery_protocols.cdp.cdp_run import run_cdp
from functions.infos.info_run import run_info
from functions.ip.ipv4.ipv4_run import run_ipv4
from functions.ip.ipv6.ipv6_run import run_ipv6
from functions.l2vni.l2vni_run import run_l2vni
from functions.mlag.mlag_run import run_mlag
from functions.mtu.mtu_run import run_mtu
from functions.ospf.ospf_run import run_ospf
from functions.ping.ping_run import run_ping
from functions.socket.socket_run import run_socket
from functions.static.static_run import run_static
from functions.vlan.vlan_run import run_vlan
from functions.vrf.vrf_run import run_vrf
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
    default=False,
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

    return (
        run_bgp(nr=nr, test_to_execute=t, reports=reports)
        and run_bgp_up(nr=nr, test_to_execute=t)
        and run_bond(nr=nr, test_to_execute=t)
        and run_lldp(nr=nr, test_to_execute=t)
        and run_cdp(nr=nr, test_to_execute=t)
        and run_info(nr=nr, test_to_execute=t)
        and run_ipv4(nr=nr, test_to_execute=t)
        and run_ipv6(nr=nr, test_to_execute=t)
        and run_l2vni(nr=nr, test_to_execute=t)
        and run_mlag(nr=nr, test_to_execute=t)
        and run_mtu(nr=nr, test_to_execute=t)
        and run_ospf(nr=nr, test_to_execute=t)
        and run_ping(nr=nr, test_to_execute=t)
        and run_socket(nr=nr, test_to_execute=t)
        and run_static(nr=nr, test_to_execute=t)
        and run_vlan(nr=nr, test_to_execute=t)
        and run_vrf(nr=nr, test_to_execute=t)
    )


if __name__ == "__main__":
    main()
