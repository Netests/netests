#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.lldp import LLDP, ListLLDP


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
                for address in n.get("managementAddresses", NOT_SET):
                    if address.get("addressType", NOT_SET) == "ipv4":
                        neighbor_mgmt_ip = address.get("address", NOT_SET)
                    if address.get("addressType", NOT_SET) == "ipv6":
                        pass

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

    return lldp_neighbors_lst
