#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET as NSET, LEVEL1
import pprint
PP = pprint.PrettyPrinter(indent=4)


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

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NSET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
