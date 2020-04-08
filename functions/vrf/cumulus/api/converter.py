#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import textfsm
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL3,
    TEXTFSM_PATH
)
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import printline
from functions.verbose_mode import (
    verbose_mode
)


def _cumulus_vrf_api_converter(hostname: str(), cmd_output) -> ListVRF:
    template = open(
        f"{TEXTFSM_PATH}cumulus_net_show_vrf.textfsm"
    )
    results_template = textfsm.TextFSM(template)
    parsed_results = results_template.ParseText(cmd_output.decode())

    list_vrf = ListVRF(list())

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        printline()
        print(parsed_results)

    for line in parsed_results:
        vrf = VRF(
            vrf_name=line[0],
            vrf_id=line[1]
        )

        list_vrf.vrf_lst.append(vrf)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(list_vrf)

    return list_vrf
