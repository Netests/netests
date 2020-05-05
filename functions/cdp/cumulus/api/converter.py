#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.cdp import CDP, ListCDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from const.constants import NOT_SET, LEVEL1, LEVEL3
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _cumulus_cdp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    if (
        'lldp' in cmd_output.keys() and
        'interface' in cmd_output.get('lldp')[0].keys()
    ):
        for l in cmd_output.get('lldp')[0].get("interface"):
            if "CDP" in l.get("via", NOT_SET):
                neighbor_type_lst = list()
                for c in l.get("chassis", NOT_SET)[0] \
                          .get("capability", NOT_SET):
                    neighbor_type_lst.append(c.get("type", NOT_SET))

                if l.get("chassis", NOT_SET)[0].get("descr", NOT_SET) == NOT_SET:
                    neighbor_os = NOT_SET
                else:
                    neighbor_os = l.get("chassis")[0] \
                                   .get("descr")[0] \
                                   .get("value", NOT_SET)

                cdp_neighbors_lst.cdp_neighbors_lst.append(
                    CDP(
                        local_name=hostname,
                        local_port=l.get("name", NOT_SET),
                        neighbor_mgmt_ip=l.get("chassis")[0]
                                          .get("mgmt-ip")[0]
                                          .get("value", NOT_SET),
                        neighbor_name=l.get("chassis")[0]
                                       .get("name")[0]
                                       .get("value", NOT_SET),
                        neighbor_port=l.get("port")[0]
                                       .get("id")[0]
                                       .get("value", NOT_SET),
                        neighbor_os=neighbor_os,
                        neighbor_type=neighbor_type_lst,
                        options=options
                    )
                )
  
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(cdp_neighbors_lst.to_json())

    return cdp_neighbors_lst
