#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    if (
        'lldp-neighbors-information' in cmd_output.keys() and
        'lldp-neighbor-information' in cmd_output.get(
            "lldp-neighbors-information")[0].keys()
    ):
        for n in cmd_output.get("lldp-neighbors-information")[0] \
                           .get("lldp-neighbor-information"):
            lldp_neighbors_lst.lldp_neighbors_lst.append(
                LLDP(
                    local_name=hostname,
                    local_port=n.get("lldp-local-port-id")[0].get("data"),
                    neighbor_name=n.get("lldp-remote-system-name")[0]
                                   .get("data"),
                    neighbor_port=n.get("lldp-remote-port-id")[0].get("data"),
                    neighbor_mgmt_ip=NOT_SET,
                    neighbor_os=NOT_SET,
                    neighbor_type=NOT_SET,
                    options=options
                )
            )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
