#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from const.constants import NOT_SET as NSET, LEVEL1
from functions.verbose_mode import verbose_mode
from functions.global_tools import printline
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _napalm_lldp_converter(
    hostname: str(),
    cmd_output: json,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    if 'get_lldp_neighbors_detail' in cmd_output.keys():
        for i, f in cmd_output.get('get_lldp_neighbors_detail').items():
            for n in f:
                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=i,
                        neighbor_mgmt_ip=NSET,
                        neighbor_name=n.get("remote_system_name", NSET),
                        neighbor_port=n.get("remote_port"),
                        neighbor_os=n.get("remote_system_description", NSET),
                        neighbor_type=n.get("remote_system_capab", NSET),
                        options=options
                    )
                )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NSET),
        needed_value=LEVEL1
    ):
        printline()
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
