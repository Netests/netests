#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocols.facts import Facts


def _juniper_facts_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> Facts:

    print(cmd_output)
