#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.cdp import CDP, ListCDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_cdp_api_converter(
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
        'ins_api' in cmd_output.keys() and
        'outputs' in cmd_output.get('ins_api').keys() and
        'output' in cmd_output.get('ins_api').get('outputs').keys() and
        'body' in cmd_output.get('ins_api')
                            .get('outputs')
                            .get('output')
                            .keys() and
        'TABLE_cdp_neighbor_detail_info' in cmd_output.get('ins_api')
                                         .get('outputs')
                                         .get('output')
                                         .get('body')
                                         .keys() and
        'ROW_cdp_neighbor_detail_info' in cmd_output.get('ins_api')
                                       .get('outputs')
                                       .get('output')
                                       .get('body')
                                       .get('TABLE_cdp_neighbor_detail_info')
                                       .keys() and
        cmd_output.get('ins_api').get('outputs').get(
            'output').get('code') == '200'
    ):
        if isinstance(
            cmd_output.get('ins_api')
                      .get('outputs')
                      .get('output')
                      .get('body')
                      .get('TABLE_cdp_neighbor_detail_info')
                      .get('ROW_cdp_neighbor_detail_info'),
            list
        ):
            for n in cmd_output.get('ins_api') \
                               .get('outputs') \
                               .get('output') \
                               .get('body') \
                               .get('TABLE_cdp_neighbor_detail_info') \
                               .get('ROW_cdp_neighbor_detail_info'):
                neighbor_type_lst = list()

                if isinstance(
                    n.get("capability"),
                    list
                ):
                    for s in n.get("capability", []):
                        if s.isalpha():
                            neighbor_type_lst.append(
                                _mapping_sys_capabilities(s)
                            )
                else:
                    neighbor_type_lst.append(
                        _mapping_sys_capabilities(
                            n.get("capability")
                        )
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
            cmd_output.get('ins_api')
                      .get('outputs')
                      .get('output')
                      .get('body')
                      .get('TABLE_cdp_neighbor_detail_info')
                      .get('ROW_cdp_neighbor_detail_info'),
            dict
        ):
            neighbor_type_lst = list()
            if isinstance(
                cmd_output.get('ins_api')
                          .get('outputs')
                          .get('output')
                          .get('body')
                          .get('TABLE_cdp_neighbor_detail_info')
                          .get('ROW_cdp_neighbor_detail_info')
                          .get("capability"),
                list
            ):
                for s in cmd_output.get('ins_api') \
                                   .get('outputs') \
                                   .get('output') \
                                   .get('body') \
                                   .get('TABLE_cdp_neighbor_detail_info') \
                                   .get('ROW_cdp_neighbor_detail_info') \
                                   .get("capability"):
                    if s.isalpha():
                        neighbor_type_lst.append(
                            _mapping_sys_capabilities(s)
                        )
            else:
                neighbor_type_lst.append(
                    _mapping_sys_capabilities(
                        cmd_output.get('ins_api')
                                  .get('outputs')
                                  .get('output')
                                  .get('body')
                                  .get('TABLE_cdp_neighbor_detail_info')
                                  .get('ROW_cdp_neighbor_detail_info')
                                  .get("capability")
                    )
                )
            n = cmd_output
            cdp_neighbors_lst.cdp_neighbors_lst.append(
                CDP(
                    local_name=hostname,
                    local_port=n.get('ins_api')
                                .get('outputs')
                                .get('output')
                                .get('body')
                                .get('TABLE_cdp_neighbor_detail_info')
                                .get('ROW_cdp_neighbor_detail_info')
                                .get("intf_id", NOT_SET),
                    neighbor_mgmt_ip=n.get('ins_api')
                                      .get('outputs')
                                      .get('output')
                                      .get('body')
                                      .get('TABLE_cdp_neighbor_detail_info')
                                      .get('ROW_cdp_neighbor_detail_info')
                                      .get("v4addr", NOT_SET),
                    neighbor_name=n.get('ins_api')
                                   .get('outputs')
                                   .get('output')
                                   .get('body')
                                   .get('TABLE_cdp_neighbor_detail_info')
                                   .get('ROW_cdp_neighbor_detail_info')
                                   .get("device_id", NOT_SET),
                    neighbor_port=n.get('ins_api')
                                   .get('outputs')
                                   .get('output')
                                   .get('body')
                                   .get('TABLE_cdp_neighbor_detail_info')
                                   .get('ROW_cdp_neighbor_detail_info')
                                   .get("port_id", NOT_SET),
                    neighbor_os=n.get('ins_api')
                                 .get('outputs')
                                 .get('output')
                                 .get('body')
                                 .get('TABLE_cdp_neighbor_detail_info')
                                 .get('ROW_cdp_neighbor_detail_info')
                                 .get("version", NOT_SET),
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
