#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import lxml
from protocols.facts import Facts
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_facts_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:
    
    print(cmd_output)
