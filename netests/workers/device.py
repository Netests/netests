#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from nornir.core.task import Task
from abc import ABC, abstractmethod
from netests.constants import VRF_DATA_KEY, VRF_DEFAULT_RT_LST


class Device(ABC):

    task: Task
    commands: dict
    """
        commands = {
            "default_vrf": {
                "key1": "show ip int brief",
                "key2": "show lldp neighbors"
            },
            "vrf": {
                "key1": "show ip ospf vrf eudhe"
            }
        }
    """
    commands_output: dict()
    vrf_loop: bool
    results: list
    converter: str
    key_store: str
    options: dict
    format_command: bool

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={},
        format_command=True,
    ):
        log.debug(
            "\n"
            f"commands={commands}\n"
            f"vrf_loop={vrf_loop}\n"
            f"converter={converter}\n"
            f"key_store={key_store}\n"
            f"options={options}\n"
            f"format_command={format_command}\n"
        )
        self.task = task
        self.commands = commands
        self.commands_output = {}
        self.vrf_loop = vrf_loop
        self.converter = converter
        self.key_store = key_store
        self.options = options
        self.results = list()
        self.format_command = format_command

    def get(self, task):
        log.debug(
            "\n"
            f"Function get(self, task)\n"
            f"hostname={task.host.name}\n"
            f"vrf_loop={self.vrf_loop}\n"
            f"self.commands.keys()={self.commands.keys()}\n"
            f"'vrf' in self.commands.keys()={'vrf' in self.commands.keys()}\n"
            "\n"
            "Use get_loop_vrf="
            f"{self.vrf_loop and 'vrf' in self.commands.keys()}\n"
            f"Use get_no_vrf={'default_vrf' in self.commands.keys()}\n"
        )

        if self.vrf_loop and "vrf" in self.commands.keys():
            self.get_loop_vrf(task)
        elif "default_vrf" in self.commands.keys():
            self.get_no_vrf(task)
        self.call_converter(task)

    @abstractmethod
    def exec_call(self, task, command, vrf):
        pass

    def get_no_vrf(self, task):
        log.debug(
            f"hostname={task.host.name}\n"
            "if 'no_key' in self.commands.get('default_vrf').keys()="
            f"{'no_key' in self.commands.get('default_vrf').keys()}\n"
        )
        if "no_key" in self.commands.get('default_vrf').keys():
            log.debug(
                "Call self.exec_call with the followings parameters : \n"
                f"hostname={task.host.name}\n"
                f" - task={task} \n"
                f" - cmd={self.commands.get('default_vrf').get('no_key')} \n"
                f" - vrf='master' \n"
            )
            self.commands_output = self.exec_call(
                task,
                self.commands.get('default_vrf').get('no_key'),
                "master"
            )
        else:
            self.commands_output = dict()
            for key, command in self.commands.get('default_vrf').items():
                log.debug(
                    "Call self.exec_call with : \n"
                    f"hostname={task.host.name}\n"
                    f" - task={task} \n"
                    f" - cmd={command} \n"
                    f" - vrf='master' \n"
                )
                self.commands_output[key] = self.exec_call(
                    task,
                    command,
                    "master"
                )

    def get_loop_vrf(self, task):
        self.commands_output = dict()
        log.debug(
            f"hostname={task.host.name}\n"
            "if 'default_vrf' in self.commands.keys()="
            f"{'default_vrf' in self.commands.keys()}\n"
        )

        if 'default_vrf' in self.commands.keys():
            if "no_key" not in self.commands.get('default_vrf').keys():
                self.commands_output['default'] = dict()

            for key, command in self.commands.get('default_vrf').items():
                if "no_key" in self.commands.get('default_vrf').keys():
                    log.debug(
                        "Call self.exec_call with : \n"
                        f"hostname={task.host.name}\n"
                        f" - task={task} \n"
                        f" - cmd={command} \n"
                        f" - vrf='master' \n"
                        "=> store in self.commands_output['default']"
                    )
                    self.commands_output['default'] = self.exec_call(
                        task,
                        command,
                        "master"
                    )
                else:
                    log.debug(
                        "Call self.exec_call with : \n"
                        f"hostname={task.host.name}\n"
                        f" - task={task} \n"
                        f" - cmd={command} \n"
                        f" - vrf='master' \n"
                        "=> store in self.commands_output[vrf.vrf_name][key]"
                        f" - key={key} \n"
                    )
                    self.commands_output['default'][key] = self.exec_call(
                        task,
                        command,
                        "master"
                    )

        log.debug(
            f"hostname={task.host.name}\n"
            "if 'vrf' in self.commands.keys()="
            f"{'vrf' in self.commands.keys()}\n"
        )
        if 'vrf' in self.commands.keys():
            for vrf in task.host[VRF_DATA_KEY].vrf_lst:
                log.debug("LOOP with the following VRF {vrf}")

                if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                    if (
                        "no_key" not in self.commands.get('vrf').keys() and
                        vrf.vrf_name not in self.commands_output.keys()
                    ):
                        self.commands_output[vrf.vrf_name] = dict()

                    for key, command in self.commands.get('vrf').items():
                        if self.format_command:
                            command_to_exec = command.format(vrf.vrf_name)
                        else:
                            command_to_exec = command

                        if "no_key" in self.commands.get('vrf').keys():
                            log.debug(
                                "Call self.exec_call with : \n"
                                f"hostname={task.host.name}\n"
                                f" - task={task} \n"
                                f" - cmd={command_to_exec} \n"
                                f" - vrf={vrf.vrf_name} \n"
                                "=> store in "
                                "self.commands_output[vrf.vrf_name]"
                            )
                            self.commands_output[vrf.vrf_name] \
                                = self.exec_call(
                                task,
                                command_to_exec,
                                vrf.vrf_name
                            )
                        else:
                            log.debug(
                                "Call self.exec_call with : \n"
                                f"hostname={task.host.name}\n"
                                f" - task={task} \n"
                                f" - cmd={command_to_exec} \n"
                                f" - vrf={vrf.vrf_name} \n"
                                "=> store in "
                                "self.commands_output[vrf.vrf_name][key]"
                                f" - key={key} \n"
                            )
                            self.commands_output[vrf.vrf_name][key] \
                                = self.exec_call(
                                task,
                                command_to_exec,
                                vrf.vrf_name
                            )

    def call_converter(self, task):
        log.debug(
            "\n"
            "CALL self.converter : \n"
            f" - self.key_store={self.key_store} \n"
            f" - converter={self.converter} \n"
            f" - hostname={task.host.name} \n"
            f" - commands_output={self.commands_output} \n"
            f" - options={self.options} \n"
        )
        task.host[self.key_store] = self.converter(
            hostname=task.host.name,
            cmd_output=self.commands_output,
            options=self.options
        )

        log.debug(
            "\n"
            "RESULT self.converter : \n"
            f" - converter={self.converter} \n"
            f" - hostname={task.host.name} \n"
            f" - commands_output={self.commands_output} \n"
            " ==> Result converter :\n"
            f"{task.host[self.key_store]}"
        )
