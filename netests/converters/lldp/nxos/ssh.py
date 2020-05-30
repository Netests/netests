#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.lldp import LLDP, ListLLDP
from netests.mappings import mapping_sys_capabilities


def _nxos_lldp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if (
        "Invalid command" not in cmd_output and
        "ERROR: No neighbour information" not in cmd_output
    ):
        if not isinstance(cmd_output, dict):
            cmd_output = json.loads(cmd_output)

        if (
            "TABLE_nbor_detail" in cmd_output.keys() and
            "ROW_nbor_detail" in cmd_output.get("TABLE_nbor_detail").keys()
        ):
            if isinstance(
                cmd_output.get('TABLE_nbor_detail')
                        .get('ROW_nbor_detail'),
                list
            ):
                for n in cmd_output.get('TABLE_nbor_detail') \
                                .get("ROW_nbor_detail"):
                    neighbor_type_lst = list()
                    for s in n.get("system_capability", []):
                        if s.isalpha():
                            neighbor_type_lst.append(
                                mapping_sys_capabilities(s)
                            )

                    lldp_neighbors_lst.lldp_neighbors_lst.append(
                        LLDP(
                            local_name=hostname,
                            local_port=n.get("l_port_id", NOT_SET),
                            neighbor_mgmt_ip=n.get("mgmt_addr", NOT_SET),
                            neighbor_name=n.get("sys_name", NOT_SET),
                            neighbor_port=n.get("port_id", NOT_SET),
                            neighbor_os=n.get("sys_desc", NOT_SET),
                            neighbor_type=neighbor_type_lst,
                            options=options
                        )
                    )
            elif isinstance(
                cmd_output.get('TABLE_nbor_detail')
                        .get('ROW_nbor_detail'),
                dict
            ):
                neighbor_type_lst = list()
                for s in cmd_output.get('TABLE_nbor_detail') \
                                   .get('ROW_nbor_detail') \
                                   .get("system_capability", []):
                    if s.isalpha():
                        neighbor_type_lst.append(
                            mapping_sys_capabilities(s)
                        )

                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=cmd_output.get('TABLE_nbor_detail')
                                             .get('ROW_nbor_detail')
                                             .get("l_port_id", NOT_SET),
                        neighbor_mgmt_ip=cmd_output.get('TABLE_nbor_detail')
                                                   .get('ROW_nbor_detail')
                                                   .get("mgmt_addr", NOT_SET),
                        neighbor_name=cmd_output.get('TABLE_nbor_detail')
                                                .get('ROW_nbor_detail')
                                                .get("sys_name", NOT_SET),
                        neighbor_port=cmd_output.get('TABLE_nbor_detail')
                                                .get('ROW_nbor_detail')
                                                .get("port_id", NOT_SET),
                        neighbor_os=cmd_output.get('TABLE_nbor_detail')
                                              .get('ROW_nbor_detail')
                                              .get("sys_desc", NOT_SET),
                        neighbor_type=neighbor_type_lst,
                        options=options
                    )
                )

    return lldp_neighbors_lst
