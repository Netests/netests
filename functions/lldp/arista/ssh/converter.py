#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.mappings import get_bgp_state_brief
from const.constants import NOT_SET, LEVEL1, LEVEL3
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)
        

    if 'lldpNeighbors' in cmd_output.keys():
        for i, f in cmd_output.get('lldpNeighbors').items():
            for n in f.get('lldpNeighborInfo'):
                n_type_lst = list()
                for sys_capability in n.get("systemCapabilities", NOT_SET):
                        n_type_lst.append((str(sys_capability).capitalize()))

                neighbor_mgmt_ip = str()
                neighbor_mgmt_ipv6 = str()
                for address in n.get("managementAddresses", NOT_SET):
                    if address.get("addressType", NOT_SET) == "ipv4":
                        neighbor_mgmt_ip = address.get("address", NOT_SET)
                    if address.get("addressType", NOT_SET) == "ipv6":
                        neighbor_mgmt_ipv6 = address.get("address", NOT_SET)

                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=i,
                        neighbor_mgmt_ip=neighbor_mgmt_ip,
                        neighbor_name=n.get("systemName", NOT_SET),
                        neighbor_port=n.get("neighborInterfaceInfo")
                                       .get("interfaceId", NOT_SET)
                                       .replace("\"", ""),
                        neighbor_os=n.get("systemDescription", NOT_SET),
                        neighbor_type=n_type_lst,
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
