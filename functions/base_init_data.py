#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from pathlib import Path
from nornir.core import Nornir
from functions.global_tools import printline
from const.constants import (
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    VRF_DATA_KEY
)


HEADER = "[netests - base_init_data.py]"
M = {
    "bgp": {
        "filename": "bgp.yml",
        "key": BGP_SESSIONS_HOST_KEY
    },
    "cdp": {
        "filename": "cdp.yml",
        "key": CDP_DATA_HOST_KEY
    },
    "facts": {
        "filename": "facts.yml",
        "key": FACTS_DATA_HOST_KEY
    },
    "lldp": {
        "filename": "lldp.yml",
        "key": LLDP_DATA_HOST_KEY
    },
    "vrf": {
        "filename": "vrf.yml",
        "key": VRF_DATA_KEY
    }
}


def create_truth_vars(nr: Nornir, protocol: str) -> None:
    for host in nr.inventory.hosts:
        printline()
        create_directories("truth_vars/")
        create_directories("truth_vars/hosts")
        create_directories(f"truth_vars/hosts/{host}")
        with open(
            f"truth_vars/hosts/{host}/{M.get(protocol).get('filename')}",
            'w'
        ) as outfile:
            yaml.dump(
                nr.inventory.hosts[host][M.get(protocol).get('key')].to_json(),
                outfile,
                default_flow_style=False
            )

        print(
            f"{HEADER} - Data Generate in "
            f"(truth_vars/hosts/{host}/{M.get(protocol).get('filename')}) "
            f"for host {host}"
        )


def create_directories(path: str) -> None:
    Path(path).mkdir(parents=True, exist_ok=True)
