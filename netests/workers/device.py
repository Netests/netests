#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from abc import ABC, abstractmethod
from nornir.plugins.functions.text import print_result


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
    def get_no_vrf(self, task):
        pass

    @abstractmethod
    def get_loop_vrf(self, task):
        pass

    def print_nr_result(self, output):
        print_result(output)

    def call_converter(self, task):
        task.host[self.key_store] = self.converter(
            hostname=task.host.name,
            cmd_output=self.commands_output,
            options=self.options
        )
