#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.facts import Facts
from netests.constants import NOT_SET


def _iosxr_facts_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    hostname = NOT_SET
    domain = NOT_SET
    version = NOT_SET
    serial = NOT_SET
    model = NOT_SET
    interfaces_lst = list()

    return Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor="Cisco",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )
