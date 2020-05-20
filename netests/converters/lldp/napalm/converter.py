#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET as NSET
from netests.protocols.lldp import LLDP, ListLLDP


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

    return lldp_neighbors_lst
