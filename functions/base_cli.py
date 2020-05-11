#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from nornir.core import Nornir
from functions.bgp.bgp_gets import get_bgp
from functions.bgp.bgp_compare import _compare_bgp
from protocols.bgp import BGPSession
from functions.cdp.cdp_get import get_cdp
from functions.cdp.cdp_compare import _compare_cdp
from protocols.cdp import CDP
from functions.facts.facts_get import get_facts
from functions.facts.facts_compare import _compare_facts
from protocols.facts import Facts
from functions.lldp.lldp_get import get_lldp
from functions.lldp.lldp_compare import _compare_lldp
from protocols.lldp import LLDP
from protocols.ospf import OSPF
from functions.ospf.ospf_compare import _compare_ospf
from functions.ospf.ospf_get import get_ospf
from protocols.ping import PING
from functions.ping.ping_get import get_ping
from functions.ping.ping_execute import execute_ping
from functions.vrf.vrf_get import get_vrf
from functions.vrf.vrf_compare import _compare_vrf
from protocols.vrf import VRF
from functions.global_tools import printline
from functions.global_tools import is_valid_ipv4_address
from exceptions.netests_cli_exceptions import NetestsCLINornirObjectIsNone
from const.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    PING_DATA_HOST_KEY,
    VRF_DATA_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


class NetestsCLI():

    ACTION = ["get", "select", "unselect", "exit", "help", "options", "more",
              "show", "print", "selected", "compare", "", "execute"]
    APRINT = ["get", "select", "unselect", "exit", "help", "options", "more",
              "show", "print", "selected", "compare", "execute"]
    AARGS = ["get", "select", "unselect", "options", "more", "show", "print",
             "help", "compare", "execute"]

    ASIMPLE = ["help", "", "selected", "exit"]

    A2ARGS = ["get", "select", "unselect", "more", "show", "print", "help",
              "compare"]

    A3ARGS = ["options"]

    AMANYARGS = ["execute"]

    MAPPING = {
        "bgp": {
            "class": BGPSession,
            "get": get_bgp,
            "compare": _compare_bgp
        },
        "cdp": {
            "class": CDP,
            "get": get_cdp,
            "compare": _compare_cdp
        },
        "facts": {
            "class": Facts,
            "get": get_facts,
            "compare": _compare_facts
        },
        "lldp": {
            "class": LLDP,
            "get": get_lldp,
            "compare": _compare_lldp
        },
        "ospf": {
            "class": OSPF,
            "get": get_ospf,
            "compare": _compare_ospf
        },
        "ping": {
            "class": PING,
            "get": get_ping,
            "compare": execute_ping
        },
        "vrf": {
            "class": VRF,
            "get": get_vrf,
            "compare": _compare_vrf
        }
    }

    nornir: Nornir
    devices: dict
    options: dict

    def __init__(
        self,
        nornir=None,
        devices=[],
        options={}
    ):
        if nornir is None:
            raise NetestsCLINornirObjectIsNone()

        self.devices = devices
        self.options = options
        self.nornir = nornir
        self.nornir.inventory.add_group("netests")
        self.print_welcome()

    def __split_user_input(self, user_input: str) -> list:
        return user_input.split(" ")

    def check_input(self, user_input: str) -> bool:
        user_input = self.__split_user_input(user_input)
        if user_input[0] not in self.ACTION:
            print("@Please select one of the following values :")
            print(f"@{self.APRINT}\n")
            return False
        else:
            return self.verify_args(user_input)

    def verify_args(self, user_input: list) -> bool:
        if len(user_input) < 2 and user_input[0] not in self.ASIMPLE:
            print("@The followings commands take some arguments :")
            print(f"@{self.AARGS}")
            return False

        if user_input[0] == "execute":
            if user_input[1] != "ping":
                print("@execute command only support ping. Use help")
            if len(user_input) < 3:
                print("@execute command take at least 2 arguments. Use help")
            elif is_valid_ipv4_address(user_input[2]) is False:
                print("@Second arguments of execute ping has to be an IPv4")

        if (
            user_input[0] == "help" and (
                len(user_input) == 1 or
                len(user_input) == 2
            )
        ):
            return True

        if user_input[0] in self.A3ARGS and len(user_input) != 3:
            print("@The following commands take three arguments :")
            print(f"@{self.A3ARGS}")
            print("@Use 'help {{ command }}' for more informations")
            return False

        if user_input[0] in self.A2ARGS and len(user_input) != 2:
            print("@The following commands take two arguments :")
            print(f"@{self.A2ARGS}")
            print("@Use 'help {{ command }}' for more informations")
            return False

        return True

    def select_action(self, user_inputs: str) -> None:
        user_inputs = self.__split_user_input(user_inputs)
        if user_inputs[0] == "help":
            self.select_help_function(user_inputs)
        if user_inputs[0] == "select":
            self.select_devices(user_inputs[1])
        if user_inputs[0] == "unselect":
            self.unselect_devices(user_inputs[1])
        if user_inputs[0] == "selected":
            self.print_devices()
        if user_inputs[0] == "get":
            if self.devices_not_empty():
                self.call_get_generic(user_inputs[1])
            else:
                print("@Please select some hosts before use get command")
        if user_inputs[0] == "options":
            self.define_options(user_inputs[1], user_inputs[2])
        if user_inputs[0] == "more":
            self.get_protocol_info(user_inputs[1])
        if user_inputs[0] == "show":
            self.get_protocol_class(user_inputs[1])
        if user_inputs[0] == "print":
            self.get_device_info(user_inputs[1])
        if user_inputs[0] == "execute":
            self.execute_ping(user_inputs)
        if user_inputs[0] == "compare":
            if self.devices_not_empty():
                self.compare_config(user_inputs[1])
            else:
                print("@Please select some hosts before use compare command")
        return True

    def execute_cli_ping(self, parameters) -> None:
        print("@execute command not Implemented ...")

    def compare_config(self, protocols_selected) -> None:
        self.call_get_generic(protocols_selected)
        w = list()

        for prot in protocols_selected.split(','):
            for d in self.devices:
                if prot.lower() == "vrf":
                    r = _compare_vrf(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        vrf_host_data=self.nornir.inventory.hosts
                                                           .get(d)
                                                           .get(VRF_DATA_KEY)
                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "cdp":
                    r = _compare_cdp(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        cdp_host_data=self.nornir.inventory
                                          .hosts
                                          .get(d)
                                          .get(CDP_DATA_HOST_KEY)
                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "facts":
                    r = _compare_facts(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        facts_host_data=self.nornir.inventory
                                                    .hosts
                                                    .get(d)
                                                   .get(FACTS_DATA_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "ping":
                    r = execute_ping(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        facts_host_data=self.nornir.inventory
                                                   .hosts
                                                   .get(d)
                                                   .get(PING_DATA_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "lldp":
                    r = _compare_lldp(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        lldp_host_data=self.nornir.inventory
                                                   .hosts
                                                   .get(d)
                                                   .get(LLDP_DATA_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "ospf":
                    r = _compare_ospf(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        ospf_host_data=self.nornir.inventory
                                                  .hosts
                                                  .get(d)
                                                  .get(OSPF_SESSIONS_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "bgp":
                    r = _compare_bgp(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        bgp_host_data=self.nornir.inventory
                                                    .hosts
                                                    .get(d)
                                                    .get(BGP_SESSIONS_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                elif prot.lower() == "bgp":
                    r = _compare_bgp(
                        host_keys=self.nornir.inventory.hosts[d].keys(),
                        hostname=d,
                        groups=self.nornir.inventory.hosts[d].groups,
                        bgp_host_data=self.nornir.inventory
                        .hosts
                        .get(d)
                        .get(BGP_SESSIONS_HOST_KEY)

                    )
                    if r:
                        w.append(d)
                else:
                    print(f"@({prot}) is unavailable from CLI.")

        printline()
        print(
            "@The following devices have the same configuration "
            f"that defined in the source of truth : \n@{w}."
        )
        printline()

    def select_help_function(self, user_input) -> bool:
        if len(user_input) == 1:
            self.print_help()
        elif len(user_input) == 2 and user_input[1] == "select":
            self.print_select_help()
        elif len(user_input) == 2 and user_input[1] == "unselect":
            self.print_unselect_help()
        elif len(user_input) == 2 and user_input[1] == "selected":
            self.print_selected_help()
        elif len(user_input) == 2 and user_input[1] == "get":
            self.print_get_help()
        elif len(user_input) == 2 and user_input[1] == "options":
            self.print_options_help()
        elif len(user_input) == 2 and user_input[1] == "more":
            self.print_more_help()
        elif len(user_input) == 2 and user_input[1] == "show":
            self.print_show_help()
        elif len(user_input) == 2 and user_input[1] == "print":
            self.print_print_help()
        elif len(user_input) == 2 and user_input[1] == "compare":
            self.print_compare_help()
        elif len(user_input) == 2 and user_input[1] == "exit":
            self.print_exit_help()
        else:
            return False
        return True

    def devices_not_empty(self) -> bool:
        return (len(self.devices) > 0)

    def unselect_devices(self, devices_unselected: str) -> None:
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
                if host not in self.nornir.inventory.hosts:
                    print(f"@Device ({host}) is not in the inventory.")

        self.print_devices()

    def select_devices(self, devices_selected) -> None:
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
                if host not in self.nornir.inventory.hosts:
                    print(f"@Device ({host}) is not in the inventory.")

        self.print_devices()

    def define_options(self, protocol, options) -> None:
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

    def get_protocol_class(self, protocol) -> None:
        for key, values in self.MAPPING.items():
            if protocol.lower() == key:
                PP.pprint((values.get('class').__annotations__))

    def get_protocol_info(self, protocol) -> None:
        if protocol in self.options.keys():
            PP.pprint(self.options.get(protocol))
        else:
            print("@All class arguments are defined as True")

    def get_device_info(self, devices) -> None:
        p = dict()
        if devices == "*":
            for host in self.nornir.inventory.hosts:
                p[host] = dict()
                p[host]['hostname'] = self.nornir.inventory \
                                          .hosts[host].hostname
                p[host]['connexion'] = self.nornir.inventory \
                                           .hosts[host]['connexion']
                p[host]['port'] = self.nornir.inventory.hosts[host].port
                p[host]['platform'] = self.nornir.inventory \
                                          .hosts[host].platform
        else:
            for host in devices.split(','):
                if host in self.nornir.inventory.hosts:
                    p[host] = dict()
                    p[host]['hostname'] = self.nornir.inventory \
                                              .hosts[host].hostname
                    p[host]['connexion'] = self.nornir.inventory \
                                               .hosts[host]['connexion']
                    p[host]['port'] = self.nornir.inventory.hosts[host].port
                    p[host]['platform'] = self.nornir.inventory \
                                              .hosts[host].platform

        PP.pprint(p)

    def call_get_generic(self, protocols_selected) -> None:
        if protocols_selected == "*":
            print("@This function is unavailable for the moment...")
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
                elif prot.lower() == "cdp":
                    get_cdp(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('cdp', {})
                        }
                    )
                elif prot.lower() == "facts":
                    get_facts(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('facts', {})
                        }
                    )
                elif prot.lower() == "lldp":
                    get_lldp(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('lldp', {})
                        }
                    )
                elif prot.lower() == "ospf":
                    get_ospf(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('ospf', {})
                        }
                    )
                elif prot.lower() == "bgp":
                    get_bgp(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('bgp', {})
                        }
                    )
                elif prot.lower() == "ping":
                    get_ping(
                        nr=self.nornir,
                        options={
                            "from_cli": True,
                            "print": self.options.get('ping', {})
                        }
                    )
                else:
                    print(f"@({prot}) is unavailable from CLI.")

    def ask_help(self) -> None:
        print("@User 'help' command to get help.")

    def print_devices(self) -> None:
        print("@Followings devices are selected :")
        print(f"@{self.devices}")

    def print_welcome(self) -> None:
        printline()
        print("Welcome to Netests CLI")
        printline()

    def print_end_get(self) -> None:
        printline()
        print("@End GET")
        printline()

    def print_help(self) -> None:
        print("+------------------------------------------------------------+")
        print("|                       Netests Help                         |")
        print("+------------------------------------------------------------+")
        print("| [help]      Display help                                   |")
        print("| [select]    Select devices on which on action will be exec |")
        print("| [unselect]  Remove a device from the selected              |")
        print("| [selected]  Show devices currently selected                |")
        print("| [get xx]   Get XX protocols informations                   |")
        print("| [options]   Set arguments that will retrieve for a Protocol|")
        print("| [more xx]  Show XX Protocol class arguments selected       |")
        print("| [show xx]  Show XX Protocol class arguments                |")
        print("| [print yy]  Show YY devices informations                   |")
        print("| [compare yy xx]  Compare device config with source of truth|")
        print("| [exit]  Quit Netests CLI                                   |")
        print("+------------------------------------------------------------+")

    def print_options_help(self) -> None:
        print("+------------------------------------------------------------+")
        print("|                 Netests - Options Commands                 |")
        print("+------------------------------------------------------------+")
        print("| This command is used to define which parameter will be     |")
        print("| retrieve for a protocol.                                   |")
        print("| It is possible to get a subset of protocols parameters.    |")
        print("| Format :                                                   |")
        print("|   > options  {{ protocol }}  {{ classArg1,classArg2  }}    |")
        print("|   (To get all protocols parameters use the 'show' command) |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > options vrf vrf_name,rd,rt_imp,rt_exp                  |")
        print("+------------------------------------------------------------+")

    def print_print_help(self):
        print("+------------------------------------------------------------+")
        print("|                 Netests - Print Commands                   |")
        print("+------------------------------------------------------------+")
        print("| This command is used to display host informations          |")
        print("| NetestsCLI is based on your inventory and retrive all your |")
        print("| hosts. With this command you can print hosts informations  |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > print {{ hostname }}  {{ hostname1,hostname2  }}       |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > print leaf01,leaf03,spine01                            |")
        print("|   > print *                                                |")
        print("+------------------------------------------------------------+")

    def print_select_help(self):
        print("+------------------------------------------------------------+")
        print("|                Netests - Select Commands                   |")
        print("+------------------------------------------------------------+")
        print("| Netests is based on your network inventory. Before to get  |")
        print("| device informations you have to select devices that you    |")
        print("| want get information. For that you need to use 'select'    |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > select {{ hostname }}  {{ hostname1,hostname2  }}      |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > select leaf01,leaf03,spine01                           |")
        print("|   > select *                                               |")
        print("+------------------------------------------------------------+")

    def print_unselect_help(self):
        print("+------------------------------------------------------------+")
        print("|              Netests - Unselect Commands                   |")
        print("+------------------------------------------------------------+")
        print("| Netests is based on your network inventory. Once you have  |")
        print("| selected some device, you can unselect some devices.       |")
        print("| For that you need to use 'unselect'                        |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > unselect {{ hostname }}  {{ hostname1,hostname2  }}    |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > unselect leaf01,leaf03,spine01                         |")
        print("|   > unselect *                                             |")
        print("+------------------------------------------------------------+")

    def print_selected_help(self):
        print("+------------------------------------------------------------+")
        print("|              Netests - Unselect Commands                   |")
        print("+------------------------------------------------------------+")
        print("| Netests is based on your network inventory. Once you have  |")
        print("| selected some device, you can print the devices currently  |")
        print("| selected. For that you need to use 'selected'              |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > unselect                                               |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > selected                                               |")
        print("+------------------------------------------------------------+")

    def print_show_help(self):
        print("+------------------------------------------------------------+")
        print("|                 Netests - Show Commands                    |")
        print("+------------------------------------------------------------+")
        print("| Each protocol is defined in a Python class.                |")
        print("| Each protocol has some variables that define it.           |")
        print("| To see all parameters that compose the protocol use 'more'.|")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > show {{ protocol }}                                    |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > show vrf                                               |")
        print("+------------------------------------------------------------+")

    def print_more_help(self):
        print("+------------------------------------------------------------+")
        print("|                 Netests - More Commands                    |")
        print("+------------------------------------------------------------+")
        print("| You can filter which parameters will be retrieve from each |")
        print("| devices for a protocol. You can filter this parameters     |")
        print("| with 'options' command. Once you have applied some filters |")
        print("| you can print which paramters are currently selected with  |")
        print("| 'more' command                                             |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > more {{ protocol }}                                    |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > show vrf                                               |")
        print("+------------------------------------------------------------+")

    def print_get_help(self):
        print("+------------------------------------------------------------+")
        print("|                  Netests - Get Commands                    |")
        print("+------------------------------------------------------------+")
        print("| Once you have selected devices, 'get' command will         |")
        print("| establish a session to the network device(s) and retrieve  |")
        print("| regarding the protocol given in argument.                  |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > get {{ protocol }}                                     |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > get vrf                                                |")
        print("+------------------------------------------------------------+")

    def print_compare_help(self):
        print("+------------------------------------------------------------+")
        print("|                 Netests - Exit Commands                    |")
        print("+------------------------------------------------------------+")
        print("| It is possible, from the CLI, to compare your network      |")
        print("| devices configuration with the configuration defined in    |")
        print("| the source of truth.                                       |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > compare {{ protocol }}                                 |")
        print("|                                                            |")
        print("| Examples :                                                 |")
        print("|   > compare vrf                                            |")
        print("|                                                            |")
        print("+------------------------------------------------------------+")

    def print_exit_help(self):
        print("+------------------------------------------------------------+")
        print("|                 Netests - Exit Commands                    |")
        print("+------------------------------------------------------------+")
        print("| Use this command to exit from Netests CLI. That's it.      |")
        print("|                                                            |")
        print("| Format :                                                   |")
        print("|   > exit                                                   |")
        print("|                                                            |")
        print("+------------------------------------------------------------+")


def netests_cli(nr) -> None:
    user_input = "START"
    cli = NetestsCLI(nornir=nr)

    while user_input != "exit":
        user_input = input("> ")

        if cli.check_input(user_input):
            cli.select_action(user_input)
