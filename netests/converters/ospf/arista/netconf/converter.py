#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.ospf import OSPF


def _arista_ospf_netconf_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:
    pass
