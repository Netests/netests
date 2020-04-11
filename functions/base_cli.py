#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.vrf.vrf_get import get_vrf
from functions.global_tools import (
    init_nornir,
    printline
)

ACTION = ["get", "select", "unselect", "exit", "help", ""]


def netests_cli(ansible, virtual, netbox):
    printline()
    print("Welcome to Netests CLI")
    printline()
    user_input = "start"
    devices = list()

    nr = init_nornir(
        log_file="./nornir/nornir.log",
        log_level="debug",
        ansible=ansible,
        virtual=virtual,
        netbox=netbox,
    )
    nr.inventory.add_group("deviceSelec")

    while user_input != "exit":
        user_input = input("> ")

        if check_input(user_input.split(" ")):
            devices = select_action(nr, user_input.split(" "), devices)

def check_input(user_input: str) -> bool:
    if user_input[0] not in ACTION:
        print("@Please select one of the following values :")
        print(f"@{ACTION}\n")
        return False
    else:
        return True

def select_action(nr, user_inputs: list, devices: list):
    if user_inputs[0] == "help":
        print("+------------------------------------------------------------+")
        print("|                       Netests Help                         |")
        print("+------------------------------------------------------------+")
        print("| [help]      Display help                                   |")
        print("| [select]    Select devices on which on action will be exec |")
        print("| [unselect]  Remove a device from the selected              |")
        print("| [get xxx]   Get XXX protocols informations                 |")
        print("+------------------------------------------------------------+")
    
    if user_inputs[0] == "select":
        print(f"@Followings devices will be added to the list :")
        devices = list()
        if user_inputs[1] == "*":
            for host in nr.inventory.hosts:
                nr.inventory.hosts[host].groups.append("deviceSelec")
                devices.append(host)
        else:
            for host in user_inputs[1].split(','):
                if host in nr.inventory.hosts:
                    nr.inventory.hosts[host].groups.append("deviceSelec")
                    devices.append(host)
                else:
                    print(f"@Device {host} not selected because not in inv.")
        print(f"@{devices}")

    if user_inputs[0] == "get":
        if user_inputs[1] == "vrf":
            get_vrf(
                nr=nr,
                filters={},
                level=None,
                own_vars={
                    "from_cli": True
                }
            )
        printline()
        print("@End GET")
        printline()

    return devices
