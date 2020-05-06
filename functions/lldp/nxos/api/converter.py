#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1, LEVEL3
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)   
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_lldp_api_converter(
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
        'ins_api' in cmd_output.keys() and
        'outputs' in cmd_output.get('ins_api').keys() and
        'output' in cmd_output.get('ins_api').get('outputs').keys() and
        'body' in cmd_output.get('ins_api')
                            .get('outputs')
                            .get('output')
                            .keys() and
        'TABLE_nbor_detail' in cmd_output.get('ins_api')
                                         .get('outputs')
                                         .get('output')
                                         .get('body')
                                         .keys() and
        'ROW_nbor_detail' in cmd_output.get('ins_api')
                                       .get('outputs')
                                       .get('output')
                                       .get('body')
                                       .get('TABLE_nbor_detail')
                                       .keys() and
        cmd_output.get('ins_api').get('outputs').get('output').get('code') == '200'
    ):
        if isinstance(
            cmd_output.get('ins_api') \
                      .get('outputs') \
                      .get('output') \
                      .get('body') \
                      .get('TABLE_nbor_detail') \
                      .get('ROW_nbor_detail'),
            list
        ):
            for n in cmd_output.get('ins_api') \
                            .get('outputs') \
                            .get('output') \
                            .get('body') \
                            .get('TABLE_nbor_detail') \
                            .get('ROW_nbor_detail'):
                neighbor_type_lst = list()
                for s in n.get("system_capability", []):
                    if s.isalpha():
                        neighbor_type_lst.append(
                            _mapping_sys_capabilities(s)
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
            cmd_output.get('ins_api')
                      .get('outputs')
                      .get('output')
                      .get('body')
                      .get('TABLE_nbor_detail')
                      .get('ROW_nbor_detail'),
            dict
        ):
            neighbor_type_lst = list()
            for s in cmd_output.get('ins_api') \
                               .get('outputs') \
                               .get('output') \
                               .get('body') \
                               .get('TABLE_nbor_detail') \
                               .get('ROW_nbor_detail') \
                               .get("system_capability", []):
                if s.isalpha():
                    neighbor_type_lst.append(
                        _mapping_sys_capabilities(s)
                    )

            lldp_neighbors_lst.lldp_neighbors_lst.append(
                LLDP(
                    local_name=hostname,
                    local_port=cmd_output.get('ins_api')
                                         .get('outputs')
                                         .get('output')
                                         .get('body')
                                         .get('TABLE_nbor_detail')
                                         .get('ROW_nbor_detail')
                                         .get("l_port_id", NOT_SET),
                    neighbor_mgmt_ip=cmd_output.get('ins_api')
                                               .get('outputs')
                                               .get('output')
                                               .get('body')
                                               .get('TABLE_nbor_detail')
                                               .get('ROW_nbor_detail')
                                               .get("mgmt_addr", NOT_SET),
                    neighbor_name=cmd_output.get('ins_api')
                                            .get('outputs')
                                            .get('output')
                                            .get('body')
                                            .get('TABLE_nbor_detail')
                                            .get('ROW_nbor_detail')
                                            .get("sys_name", NOT_SET),
                    neighbor_port=cmd_output.get('ins_api')
                                            .get('outputs')
                                            .get('output')
                                            .get('body')
                                            .get('TABLE_nbor_detail')
                                            .get('ROW_nbor_detail')
                                            .get("port_id", NOT_SET),
                    neighbor_os=cmd_output.get('ins_api')
                                          .get('outputs')
                                          .get('output')
                                          .get('body')
                                          .get('TABLE_nbor_detail')
                                          .get('ROW_nbor_detail')
                                          .get("sys_desc", NOT_SET),
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
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
