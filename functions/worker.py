#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from nornir.core import Nornir
from nornir.core.filter import F

class Worker(ABC):
    
    nr: Nornir
    options: dict
    from_cli: bool
    verbose: str

    def __init__(self, nr, options, verbose, from_cli=False):
        self.nr = nr
        self.options = options
        self.verbose = verbose
        self.from_cli = from_cli

    def init_inventory(self):
        if self.is_from_cli():
            self.devices = nr.filter(F(groups__contains="netests"))
        else:
            self.devices = nr.filter()

    def inventory_empty(self):
        if len(self.devices.inventory.hosts) == 0:
            print("[Worker] no device selected.")

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def generic_ospf_get(self):
        pass

    def is_from_cli(self):
        return self.is_from_cli

    def print_output(self):
        pass

    
