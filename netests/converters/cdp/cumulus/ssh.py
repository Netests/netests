#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.cdp import CDP, ListCDP


def _cumulus_cdp_ssh_converter(
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
        for lldp in cmd_output.get('lldp')[0].get("interface"):
            if "CDP" in lldp.get("via", NOT_SET):
                neighbor_type_lst = list()
                for c in lldp.get("chassis", NOT_SET)[0] \
                             .get("capability", NOT_SET):
                    neighbor_type_lst.append(c.get("type", NOT_SET))

                if lldp.get("chassis", NOT_SET)[0] \
                       .get("descr", NOT_SET) == NOT_SET:
                    neighbor_os = NOT_SET
                else:
                    neighbor_os = lldp.get("chassis")[0] \
                                      .get("descr")[0] \
                                      .get("value", NOT_SET)

                cdp_neighbors_lst.cdp_neighbors_lst.append(
                    CDP(
                        local_name=hostname,
                        local_port=lldp.get("name", NOT_SET),
                        neighbor_mgmt_ip=lldp.get("chassis")[0]
                                          .get("mgmt-ip")[0]
                                          .get("value", NOT_SET),
                        neighbor_name=lldp.get("chassis")[0]
                                       .get("name")[0]
                                       .get("value", NOT_SET),
                        neighbor_port=lldp.get("port")[0]
                                       .get("id")[0]
                                       .get("value", NOT_SET),
                        neighbor_os=neighbor_os,
                        neighbor_type=neighbor_type_lst,
                        options=options
                    )
                )

    return cdp_neighbors_lst
