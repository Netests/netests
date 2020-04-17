#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import lxml
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL1,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _ios_facts_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:
    pass
