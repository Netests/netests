#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
import shutil
from netests import log
from pathlib import Path
from nornir.core import Nornir
from nornir.core.filter import F
from abc import ABC, abstractmethod
from netests.constants import PLATFORM_SUPPORTED, CONNEXION_MODE
from netests.exceptions.netests_exceptions import (
    NetestsDeviceNotCompatibleWithNapalm
)
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
    filename: str
    protocol: str
    key_store: str
    compare_result: dict

    HEADER = "[netests - GetterBase]"
    NOT_SET = "NOT_SET"
    MAPPING_FUNCTION = {}
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
        filename="",
        protocol="",
        key_store=""
    ):
        log.debug(
            "\n"
            f"Init new Object : <{self.__class__.__name__}>\n"
            f"options={options}\n"
            f"from_cli={from_cli}\n"
            f"num_workers={num_workers}\n"
            f"print_task_output={print_task_output}\n"
            f"filename={filename}\n"
            f"protocol={protocol}\n"
            f"key_store={key_store}\n"
        )
        self.nr = nr
        self.options = options
        self.from_cli = from_cli if from_cli is not None else False
        self.num_workers = num_workers if num_workers != self.NOT_SET else 50
        self.verbose = verbose if verbose != self.NOT_SET else self.LEVEL0
        self.print_task_output = print_task_output
        self.filename = filename
        self.protocol = protocol
        self.key_store = key_store
        self.devices = self.select_devices()
        self.hosts = self.devices.inventory.hosts
        self.compare_result = dict()

    @abstractmethod
    def init_mapping_function(self):
        pass

    @abstractmethod
    def compare(self):
        pass

    def _compare_result(self, data):
        log.debug(
            f"RESULT - {self.__class__.__name__}"
            f"data.values()={data.values()}"
        )
        for value in data.values():
            self.compare_result[value.host] = value.result
        log.debug(
            f"RESULT - {self.__class__.__name__}"
            f"self.compare_result={self.compare_result}"
        )

    def get_compare_result(self):
        return self.compare_result

    def print_compare_result(self):
        self.printline()
        self.print_json(self.compare_result)

    def run(self):
        log.debug("Run <generic_get>")
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def init_data(self) -> None:
        for host in self.nr.inventory.hosts:
            if self.key_store in self.nr.inventory.hosts[host].keys():
                self.create_directories("truth_vars/")
                self.create_directories("truth_vars/hosts")
                self.create_directories(f"truth_vars/hosts/{host}")
                with open(
                    f"truth_vars/hosts/{host}/{self.filename}",
                    'w'
                ) as outfile:
                    log.debug(
                        "\n"
                        "Write the following data into "
                        f"truth_vars/hosts/{host}/{self.filename}"
                        "\n"
                        "" + str(self.nr.inventory.hosts.get(host)
                                                        .get(self.key_store)
                                                        .to_json())
                    )
                    yaml.dump(
                        self.nr.inventory.hosts.get(host)
                                               .get(self.key_store)
                                               .to_json(),
                        outfile,
                        default_flow_style=False
                    )

    def create_directories(self, path: str) -> None:
        log.debug(f"Create new folder if not exist {path}")
        Path(path).mkdir(parents=True, exist_ok=True)

    def print_result(self):
        log.debug(f"Print informations {self.key_store} - {self.protocol}")
        self.print_protocols_result(self.key_store, self.protocol)

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
        log.debug(
            "\n"
            f"host={task.host.name}\n"
            f"platform={task.host.platform}\n"
            f"connexion={task.host.data.get('connexion')}\n"
        )
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
        log.debug(functions_mapping.get(platform).get(connection_mode))
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

    def function_not_implemented(self, task):
        log.debug("Function not implemented")

    def __repr__(self) -> str:
        pass

    def to_json(self) -> dict:
        pass
