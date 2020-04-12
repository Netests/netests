#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import inspect
from nornir.core import Nornir
from functions.vrf.vrf_get import get_vrf
from protocols.vrf import VRF
from functions.global_tools import (
    init_nornir,
    printline
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


class NetestsCLI():

    ACTION = ["get", "select", "unselect", "exit", "help", "options", "more", "show", ""]
    ACTION_PRINT = ["get", "select", "unselect", "exit", "help", "options", "more", "show"]

    MAPPING = {
        "vrf": {
            "class": VRF,
            "get": get_vrf
        }
    }

    nornir: Nornir
    devices: dict
    options: dict

    def __init__(
        self,
        devices=[],
        options={},
        ansible=False,
        virtual=False,
        netbox=False
    ):
        self.devices = devices
        self.options = options
        self.nornir = init_nornir(
            log_file="./nornir/nornir.log",
            log_level="debug",
            ansible=ansible,
            virtual=virtual,
            netbox=netbox,
        )
        self.nornir.inventory.add_group("netests")
        self.__print_welcome()

    def check_input(self, user_input=list) -> bool:
        if user_input[0] not in self.ACTION:
            print("@Please select one of the following values :")
            print(f"@{self.ACTION_PRINT}\n")
            return False
        else:
            return True

    def select_action(self, user_inputs: list):
        if user_inputs[0] == "help":
            self.__print_help()
        if user_inputs[0] == "select":
            self.__select_devices(user_inputs[1])
        if user_inputs[0] == "unselect":
            self.__unselect_devices(user_inputs[1])
        if user_inputs[0] == "get":
            self.__call_get_generic(user_inputs[1])
        if user_inputs[0] == "options":
            self.__define_options(user_inputs[1], user_inputs[2])
        if user_inputs[0] == "more":
            self.__get_protocol_info(user_inputs[1])
        if user_inputs[0] == "show":
            self.__get_protocol_class(user_inputs[1])
        
    def __unselect_devices(self, devices_unselected):
        if devices_unselected == "*":
            for host in self.nornir.inventory.hosts:
                if (
                    host in self.devices and
                    'netests' in self.nornir.inventory.hosts[host].groups
                ):
                    self.nornir.inventory.hosts[host].groups.remove("netests")
                    self.devices.remove(host)
        else:
            for host in devices_unselected.split(','):
                if (
                    host in self.devices and
                    host in self.nornir.inventory.hosts and
                    'netests' in self.nornir.inventory.hosts[host].groups
                ):
                    self.nornir.inventory.hosts[host].groups.remove("netests")
                    self.devices.remove(host)

        self.__print_devices()

    def __select_devices(self, devices_selected):
        if devices_selected == "*":
            for host in self.nornir.inventory.hosts:
                if (
                    host not in self.devices and
                    'netests' not in self.nornir.inventory.hosts[host].groups
                ):
                    self.nornir.inventory.hosts[host].groups.append("netests")
                    self.devices.append(host)
        else:
            for host in devices_selected.split(','):
                if (
                    host not in self.devices and
                    host in self.nornir.inventory.hosts and 
                    'netests' not in self.nornir.inventory.hosts[host].groups
                ):
                    self.nornir.inventory.hosts[host].groups.append("netests")
                    self.devices.append(host)
        
        self.__print_devices()

    def __define_options(self, protocol, options):
        for key, values in self.MAPPING.items():
            if protocol.lower() == key:
                if options == "*":
                    if protocol in self.options.keys():
                        del self.options[protocol]
                    print(f"@All options are added to ({protocol})")
                else:
                    for opt in options.split(','):
                        if opt in values.get('class').__annotations__.keys():
                            if key not in self.options.keys():
                                self.options[key] = dict()
                            self.options[key][opt] = True
                
                    for v in values.get('class').__annotations__.keys():
                        if v not in options.split(','):
                            self.options[key][v] = False

                    print(f"@New ({key}) options are :")
                    PP.pprint(self.options.get(key))

    def __get_protocol_class(self, protocol):
        for key, values in self.MAPPING.items():
            if protocol.lower() == key:
                PP.pprint((values.get('class').__annotations__))

    def __get_protocol_info(self, protocol):
        if protocol in self.options.keys():
            PP.pprint(self.options.get(protocol))
        else:
            print(f"@All class arguments are defined as True")

    def __call_get_generic(self, protocols_selected):
        if protocols_selected == "*":
            print(f"@This function is unavailable for the moment...")
        else:
            for prot in protocols_selected.split(','):
                if prot.lower() == "vrf":
                    get_vrf(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('vrf', {})
                        }
                    )

                else: 
                    print(f"@({prot}) is unavailable from CLI for the moment.")

    def __print_devices(self):
        print(f"@Followings devices are selected :")
        print(f"@{self.devices}")
    
    def __print_welcome(self):
        printline()
        print("Welcome to Netests CLI")
        printline()

    def __print_end_get(self):
        printline()
        print("@End GET")
        printline()

    def __print_help(self):
        print("+------------------------------------------------------------+")
        print("|                       Netests Help                         |")
        print("+------------------------------------------------------------+")
        print("| [help]      Display help                                   |")
        print("| [select]    Select devices on which on action will be exec |")
        print("| [unselect]  Remove a device from the selected              |")
        print("| [get xxx]   Get XXX protocols informations                 |")
        print("+------------------------------------------------------------+")



def netests_cli(ansible, virtual, netbox):
    user_input = "START"
    cli = NetestsCLI(
        ansible=ansible,
        virtual=virtual,
        netbox=netbox
    )   

    while user_input != "exit":
        user_input = input("> ")

        if cli.check_input(user_input.split(" ")):
            cli.select_action(user_input.split(" "))
