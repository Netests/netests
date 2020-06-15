#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Dict, Optional
from pydantic import BaseModel
from abc import ABC, abstractmethod
import pprint
PP = pprint.PrettyPrinter(indent=4)


class NetestsProtocol(ABC, BaseModel):
    options: Optional[Dict[str, Dict[str, bool]]] = {}

    @abstractmethod
    def to_json(self):
        pass

    def print_json(self):
        PP.pprint(self.to_json())
