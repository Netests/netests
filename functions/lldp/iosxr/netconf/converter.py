#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL1, LEVEL4
from protocols.lldp import ListLLDP
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _iosxr_lldp_netconf_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> ListLLDP:

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    cmd_output = format_xml_output(cmd_output)
    if verbose_mode(
        user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        PP.pprint(cmd_output)

    PP.pprint(cmd_output)

    if verbose_mode(
        user_value=os.environ.get('NETESTS_VERBOSE', NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f'>>>>> {hostname}')
        PP.pprint(lldp_neighbors_lst.to_json())

    return lldp_neighbors_lst
