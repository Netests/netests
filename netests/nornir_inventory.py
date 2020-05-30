#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from nornir import InitNornir
from nornir.core import Nornir


def init_nornir(
    log_file: str,
    log_level: str,
    ansible_inventory: bool,
    nornir_inventory: bool,
    netbox_inventory: bool,
    num_workers: int,
    inventory_config_file: bool,
    inventory: str,
    nornir_groups_file: str,
    nornir_defaults_file: str,
    netbox_url: str,
    netbox_token: str,
    netbox_ssl: str
) -> Nornir:
    """
    Initialize Nornir object with the following files
    """

    log.debug(
        "\n"
        f"Inventory : ansible_inventory={ansible_inventory}\n"
        f"Inventory : nornir_inventory={nornir_inventory}\n"
        f"Inventory : netbox_inventory={netbox_inventory}\n"
        f"Nornir Setup : num_workers={num_workers}\n"
        f"Nornir Setup : inventory_config_file={inventory_config_file}\n"
        f"Nornir Setup : inventory={inventory}\n"
        f"Nornir Setup : nornir_groups_file={nornir_groups_file}\n"
        f"Nornir Setup : nornir_defaults_file={nornir_defaults_file}\n"
        f"Netbox Setup : netbox_url={netbox_url}\n"
        f"Netbox Setup : netbox_token={netbox_token}\n"
        f"Netbox Setup : netbox_ssl={netbox_ssl}\n"
    )

    config_file = ""
    plugin = ""
    options = ""

    if nornir_inventory:
        if inventory_config_file:
            config_file = ".nornir/config_nornir.yml"
        else:
            plugin = "nornir.plugins.inventory.simple.SimpleInventory"
            options = {
                "host_file": inventory,
                "group_file": nornir_groups_file,
                "defaults_file": nornir_defaults_file
            }
    elif netbox_inventory:
        if inventory_config_file:
            config_file = ".nornir/config_netbox.yml"
        else:
            plugin = "nornir.plugins.inventory.netbox.NBInventory"
            options = {
                "nb_url": netbox_url,
                "nb_token": netbox_token,
                "ssl_verify": netbox_ssl
            }
    elif ansible_inventory is not False:
        if inventory_config_file:
            config_file = ".nornir/config_ansible.yml"
        else:
            plugin = "nornir.plugins.inventory.ansible.AnsibleInventory"
            options = {
                "hostsfile": inventory
            }

    log.debug(
        "\n"
        f"Init_Nornir : num_workers={num_workers}\n"
        f"Init_Nornir : plugin={plugin}\n"
        f"Init_Nornir : options={options}\n"
        f"Init_Nornir : log_file={log_file}\n"
        f"Init_Nornir : log_level={log_level}\n"
        f"Init_Nornir : config_file={config_file}\n"
    )

    nr = InitNornir(
        core={"num_workers": num_workers},
        inventory={"plugin": plugin, "options": options},
        logging={"file": log_file, "level": log_level}
    )

    return nr
