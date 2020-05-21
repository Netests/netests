#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from abc import ABC, abstractmethod
from nornir.plugins.functions.text import print_result
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

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={}
    ):
        self.task = task
        self.commands = commands
        self.commands_output = {}
        self.vrf_loop = vrf_loop
        self.converter = converter
        self.key_store = key_store
        self.options = options
        self.results = list()

    def get(self, task):
        if self.vrf_loop and "vrf" in self.commands.keys():
            self.get_loop_vrf(task)
        elif "default_vrf" in self.commands.keys():
            self.get_no_vrf(task)
        self.call_converter(task)

    @abstractmethod
    def exec_call(self, task, command):
        pass

    def get_no_vrf(self, task):
        if "no_key" in self.commands.get('default_vrf').keys():
            self.commands_output = self.exec_call(
                task,
                self.commands.get('default_vrf').get('no_key')
            )
        else:
            self.commands_output = dict()
            for key, command in self.commands.get('default_vrf').items():
                self.commands_output[key] = self.exec_call(task, command)

    def get_loop_vrf(self, task):
        self.commands_output = dict()
        if 'default_vrf' in self.commands.keys():
            if "no_key" not in self.commands.get('default_vrf').keys():
                self.commands_output['default'] = dict()

            for key, command in self.commands.get('default_vrf').items():
                if "no_key" in self.commands.get('default_vrf').keys():
                    self.commands_output['default'] = self.exec_call(
                        task,
                        command
                    )
                else:
                    self.commands_output['default'][key] = self.exec_call(
                        task,
                        command
                    )

        if 'vrf' in self.commands.keys():
            for vrf in task.host[VRF_DATA_KEY].vrf_lst:
                if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                    if (
                        "no_key" not in self.commands.get('vrf').keys() and
                        vrf.vrf_name not in self.commands_output.keys()
                    ):
                        self.commands_output[vrf.vrf_name] = dict()
                for key, command in self.commands.get('vrf').items():    
                    if "no_key" in self.commands.get('vrf').keys():
                        self.commands_output[vrf.vrf_name] = self.exec_call(
                            task,
                            command.format(vrf.vrf_name)
                        )
                    else:
                        self.commands_output[vrf.vrf_name][key] = self.exec_call(
                            task,
                            command.format(vrf.vrf_name)
                        )


    def print_nr_result(self, output):
        print_result(output)

    def call_converter(self, task):
        task.host[self.key_store] = self.converter(
            hostname=task.host.name,
            cmd_output=self.commands_output,
            options=self.options
        )
