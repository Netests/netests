#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import shutil
from abc import ABC, abstractmethod
from nornir.core import Nornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from netests.exceptions.netests_exceptions import NetestsDeviceNotCompatibleWithNapalm
from netests.constants import PLATFORM_SUPPORTED, CONNEXION_MODE
import pprint
PP = pprint.PrettyPrinter(indent=4)


class GetterBase(ABC):

    nr: Nornir
    options: dict
    from_cli: str
    num_worker: int
    verbose: str
    devices: str
    print_task_output: bool
    compare: bool

    HEADER = "[netests - GetterBase]"
    NOT_SET = "NOT_SET"
    MAPPING_FUNCTION = {}
    LEVEL0 = "level0"
    LEVEL1 = "level1"
    LEVEL2 = "level2"
    LEVEL3 = "level3"
    LEVEL4 = "level4"
    LEVEL5 = "level5"
    NETCONF_CONNECTION = "netconf"
    SSH_CONNECTION = "ssh"
    API_CONNECTION = "api"
    NAPALM_CONNECTION = "napalm"
    CONNEXION_MODE = [
        NETCONF_CONNECTION,
        SSH_CONNECTION,
        API_CONNECTION,
        NAPALM_CONNECTION
    ]
    JUNOS_PLATEFORM_NAME = 'junos'
    CUMULUS_PLATEFORM_NAME = 'linux'
    NEXUS_PLATEFORM_NAME = 'nxos'
    CISCO_IOS_PLATEFORM_NAME = 'ios'
    CISCO_IOSXR_PLATEFORM_NAME = 'iosxr'
    ARISTA_PLATEFORM_NAME = 'eos'
    EXTREME_PLATEFORM_NAME = 'extreme_vsp'

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers=NOT_SET,
        verbose=NOT_SET,
        print_task_output=True,
        compare=False
    ):
        self.nr = nr
        self.options = options
        self.from_cli = from_cli if from_cli is not None else False
        self.num_workers = num_workers if num_workers != self.NOT_SET else 50
        self.verbose = verbose if verbose != self.NOT_SET else self.LEVEL0
        self.print_task_output = print_task_output
        self.compare = compare
        self.devices = self.select_devices()
        self.hosts = self.devices.inventory.hosts
        
    @abstractmethod
    def print_result(self):
        pass

    @abstractmethod
    def init_mapping_function(self):
        pass

    @abstractmethod
    def print_result(self):
        pass

    def run(self):
        output = self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        print_result(output)
        self.print_result()

    def print_protocols_result(self, pkey, protocol):
        self.printline()
        if self.print_task_output:
            for host in self.devices.inventory.hosts:
                self.printline()
                print(f">>>>> {host} -- ({protocol})")
                if (
                    pkey in self.devices
                                .inventory
                                .hosts
                                .get(host)
                                .keys() and
                    self.print_task_output is True
                ):
                    self.print_json(
                        self.devices.inventory.hosts.get(host)
                                                    .get(pkey)
                                                    .to_json()
                    )
                else:
                    print("No value found for this host.")

    def compare(self):
        pass

    def print_json(self, data):
        PP.pprint(data)

    def select_devices(self):
        if self.is_from_cli():
            return self.nr.filter(F(groups__contains="netests"))
        else:
            return self.nr.filter()

    def is_there_no_device_selected(self):
        return len(self.devices.inventory.hosts) == 0

    def is_from_cli(self):
        return self.from_cli

    def generic_get(self, task):
        worker = self.base_selection(
            platform=task.host.platform,
            connection_mode=task.host.data.get("connexion"),
            functions_mapping=self.MAPPING_FUNCTION
        )(task, self.options)
        worker.get(task)

    def base_selection(
        self,
        platform: str,
        connection_mode: str,
        functions_mapping: dict
    ):
        print(functions_mapping.get(platform).get(connection_mode))
        return functions_mapping.get(platform).get(connection_mode)

    def printline(self):
        size = int(shutil.get_terminal_size()[0] / 2)
        print("-*" * size)

    def device_not_compatible_with_napalm(self):
        raise NetestsDeviceNotCompatibleWithNapalm()

    def host_vars_ok(
        self,
        hostname: str,
        platform: str,
        connection_mode: str
    ) -> bool:
        if (
            platform in PLATFORM_SUPPORTED and
            connection_mode in CONNEXION_MODE
        ):
            return True
        else:
            print(
                f"{self.HEADER} ({hostname}) Connexion type not allowed  \n"
                f"{self.HEADER} Connexion must be one of the followings: \n"
                f"{self.HEADER} {CONNEXION_MODE}"
            )
        return False

    def __repr__(self) -> str:
        pass

    def to_json(self) -> dict:
        pass
