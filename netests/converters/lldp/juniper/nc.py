#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.protocols.lldp import LLDP, ListLLDP


def _juniper_lldp_nc_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if not isinstance(cmd_output, dict):
        cmd_output = format_xml_output(cmd_output)

    if (
        'lldp-neighbors-information' in cmd_output.keys() and
        'lldp-neighbor-information' in cmd_output.get(
            "lldp-neighbors-information").keys()
    ):
        if isinstance(
            cmd_output.get("lldp-neighbors-information")
                      .get("lldp-neighbor-information"),
            dict
        ):
            lldp_neighbors_lst.lldp_neighbors_lst.append(
                LLDP(
                    local_name=hostname,
                    local_port=cmd_output.get("lldp-neighbors-information")
                                         .get("lldp-neighbor-information")
                                         .get("lldp-local-port-id"),
                    neighbor_name=cmd_output.get("lldp-neighbors-information")
                                            .get("lldp-neighbor-information")
                                            .get("lldp-remote-system-name"),
                    neighbor_port=cmd_output.get("lldp-neighbors-information")
                                            .get("lldp-neighbor-information")
                                            .get("lldp-remote-port-id"),
                    neighbor_mgmt_ip=NOT_SET,
                    neighbor_os=NOT_SET,
                    neighbor_type=NOT_SET,
                    options=options
                )
            )
        if isinstance(
            cmd_output.get("lldp-neighbors-information")
                      .get("lldp-neighbor-information"),
            list
        ):
            for n in cmd_output.get("lldp-neighbors-information") \
                               .get("lldp-neighbor-information"):
                lldp_neighbors_lst.lldp_neighbors_lst.append(
                    LLDP(
                        local_name=hostname,
                        local_port=n.get("lldp-local-port-id"),
                        neighbor_name=n.get("lldp-remote-system-name"),
                        neighbor_port=n.get("lldp-remote-port-id"),
                        neighbor_mgmt_ip=NOT_SET,
                        neighbor_os=NOT_SET,
                        neighbor_type=NOT_SET,
                        options=options
                    )
                )

    return lldp_neighbors_lst
