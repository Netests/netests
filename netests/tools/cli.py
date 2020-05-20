#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import textfsm
from netests.constants import TEXTFSM_PATH


def parse_textfsm(content, template_file) -> list:
    template = open(
        f"{TEXTFSM_PATH}{template_file}")
    results_template = textfsm.TextFSM(template)
    return results_template.ParseText(content)
