#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL1, LEVEL3
from functions.discovery_protocols.discovery_functions import (
    _mapping_sys_capabilities
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _extreme_vsp_lldp_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    if (
        'openconfig-lldp:interfaces' in cmd_output.keys() and
        'interface' in cmd_output.get('openconfig-lldp:interfaces').keys()
    ):
        for i in cmd_output.get('openconfig-lldp:interfaces').get('interface'):
            if (
                'neighbors' in i.keys() and
                'neighbor' in i.get('neighbors').keys()
            ):
                for n in i.get('neighbors').get('neighbor'):

                    if (
                        'capabilities' in n.keys() and
                        'capability' in n.get('capabilities').keys()
                    ):
                        for c in n.get('capabilities').get('capability'):
                            pass

                    lldp_neighbors_lst.lldp_neighbors_lst.append(
                        LLDP(
                            local_name=hostname,
                            local_port=i.get('name'),
                            neighbor_mgmt_ip=n.get('state')
                                              .get('management-address'),
                            neighbor_name=n.get('state')
                                           .get('system-name'),
                            neighbor_port=n.get('state')
                                           .get('port-id'),
                            neighbor_os=n.get('state')
                                           .get('system-description'),
                            neighbor_type=NOT_SET
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


