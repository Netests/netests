#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocols.ospf import OSPF


def _cumulus_ospf_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    print(cmd_output)
