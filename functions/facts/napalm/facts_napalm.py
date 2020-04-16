#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import napalm_get
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.facts.napalm.converter import _napalm_facts_converter
from const.constants import NOT_SET, LEVEL2, ARISTA_PLATEFORM_NAME, FACTS_DATA_HOST_KEY, FACTS_SYS_DICT_KEY, FACTS_SNMP_DICT_KEY


def _generic_facts_napalm(task, options={}):
    outputs_dict = dict()
    output = task.run(
        name=f"NAPALM napalm_get_facts {task.host.platform}",
        task=napalm_get,
        getters=["facts"]
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        printline()
        print_result(output)

    task.host[FACTS_DATA_HOST_KEY] = _napalm_facts_converter(
        hostname=task.host.hostname,
        platform=task.host.platform,
        cmd_output=output.result,
        options=options
    )

