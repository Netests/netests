#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET as NSET
from netests.protocols.lldp import LLDP, ListLLDP


def _cumulus_lldp_ssh_converter(
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
        "lldp" in cmd_output.keys() and
        "interface" in cmd_output.get('lldp')[0].keys()
    ):
        for nei in cmd_output.get('lldp')[0].get("interface"):
            if nei.get("via", NSET) == "LLDP":
                neighbor_type_lst = list()
                for c in nei.get("chassis", NSET)[0] \
                            .get("capability", NSET):
                    neighbor_type_lst.append(c.get("type", NSET))

                if nei.get("chassis", NSET)[0].get("descr", NSET) == NSET:
                    neighbor_os = NSET
                else:
                    neighbor_os = nei.get("chassis")[0] \
                                     .get("descr")[0] \
                                     .get("value", NSET)

                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=nei.get("name", NSET),
                        neighbor_mgmt_ip=nei.get("chassis")[0]
                                            .get("mgmt-ip")[0]
                                            .get("value", NSET),
                        neighbor_name=nei.get("chassis")[0]
                                         .get("name")[0]
                                         .get("value", NSET),
                        neighbor_port=nei.get("port")[0]
                                         .get("id")[0]
                                         .get("value", NSET),
                        neighbor_os=neighbor_os,
                        neighbor_type=neighbor_type_lst,
                        options=options
                    )
                )

    return lldp_neighbors_lst
