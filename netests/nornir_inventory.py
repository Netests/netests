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

    config_file = ""
    plugin = ""
    options = ""

    if nornir_inventory:
        if inventory_config_file:
            config_file = ".nornir/config_netbox.yml"
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
            config_file = ".nornir/config_netbox.yml"
        else:
            plugin = "nornir.plugins.inventory.ansible.AnsibleInventory"
            options = {
                "hostsfile": inventory
            }

    nr = InitNornir(
        core={"num_workers": num_workers},
        inventory={"plugin": plugin, "options": options},
        logging={"file": log_file, "level": log_level}
    )

    return nr
