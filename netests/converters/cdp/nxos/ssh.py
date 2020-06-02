#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.protocols.cdp import CDP, ListCDP
from netests.constants import NOT_SET
from netests.mappings import mapping_sys_capabilities


def _nxos_cdp_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListCDP:

    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    if cmd_output != "":
        if not isinstance(cmd_output, dict):
            cmd_output = json.loads(cmd_output)

        if (
            "TABLE_cdp_neighbor_detail_info" in cmd_output.keys() and
            "ROW_cdp_neighbor_detail_info" in cmd_output.get(
                "TABLE_cdp_neighbor_detail_info").keys()
        ):
            if isinstance(
                cmd_output.get('TABLE_cdp_neighbor_detail_info')
                        .get('ROW_cdp_neighbor_detail_info'),
                list
            ):
                for n in cmd_output.get('TABLE_cdp_neighbor_detail_info') \
                                .get("ROW_cdp_neighbor_detail_info"):
                    neighbor_type_lst = list()
                    if isinstance(
                        n.get("capability"),
                        list
                    ):
                        for s in n.get("capability"):
                            if s.isalpha():
                                neighbor_type_lst.append(
                                    mapping_sys_capabilities(s)
                                )
                    else:
                        neighbor_type_lst.append(
                            mapping_sys_capabilities(n.get("capability"))
                        )

                    cdp_neighbors_lst.cdp_neighbors_lst.append(
                        CDP(
                            local_name=hostname,
                            local_port=n.get("intf_id", NOT_SET),
                            neighbor_mgmt_ip=n.get("v4addr", NOT_SET),
                            neighbor_name=n.get("device_id", NOT_SET),
                            neighbor_port=n.get("port_id", NOT_SET),
                            neighbor_os=n.get("version", NOT_SET),
                            neighbor_type=neighbor_type_lst,
                            options=options
                        )
                    )
            elif isinstance(
                cmd_output.get('TABLE_cdp_neighbor_detail_info')
                        .get('ROW_cdp_neighbor_detail_info'),
                dict
            ):
                neighbor_type_lst = list()
                if isinstance(
                    cmd_output.get('TABLE_cdp_neighbor_detail_info')
                            .get('ROW_cdp_neighbor_detail_info')
                            .get("capability"),
                    list
                ):
                    for s in cmd_output.get('TABLE_cdp_neighbor_detail_info') \
                                    .get('ROW_cdp_neighbor_detail_info') \
                                    .get("capability"):
                        if s.isalpha():
                            neighbor_type_lst.append(
                                mapping_sys_capabilities(s)
                            )
                else:
                    neighbor_type_lst.append(
                        mapping_sys_capabilities(
                            cmd_output.get('TABLE_cdp_neighbor_detail_info')
                                    .get('ROW_cdp_neighbor_detail_info')
                                    .get("capability"))
                    )

                n = cmd_output
                cdp_neighbors_lst.cdp_neighbors_lst.append(
                    CDP(
                        local_name=hostname,
                        local_port=n.get('TABLE_cdp_neighbor_detail_info')
                                    .get('ROW_cdp_neighbor_detail_info')
                                    .get("intf_id", NOT_SET),
                        neighbor_mgmt_ip=n
                                        .get('TABLE_cdp_neighbor_detail_info')
                                        .get('ROW_cdp_neighbor_detail_info')
                                        .get("v4addr", NOT_SET),
                        neighbor_name=n.get('TABLE_cdp_neighbor_detail_info')
                                    .get('ROW_cdp_neighbor_detail_info')
                                    .get("device_id", NOT_SET),
                        neighbor_port=n.get('TABLE_cdp_neighbor_detail_info')
                                    .get('ROW_cdp_neighbor_detail_info')
                                    .get("port_id", NOT_SET),
                        neighbor_os=n.get('TABLE_cdp_neighbor_detail_info')
                                    .get('ROW_cdp_neighbor_detail_info')
                                    .get("version", NOT_SET),
                        neighbor_type=neighbor_type_lst,
                        options=options
                    )
                )

    return cdp_neighbors_lst
