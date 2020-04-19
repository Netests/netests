#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_extreme_vsp
from functions.facts.extreme_vsp.api.converter import (
    _extreme_vsp_facts_api_converter
)
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DATA_HOST_KEY
)
from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _extreme_vsp_get_facts_api(task, options={}):
    output_dict = dict()
    output_dict[FACTS_SYS_DICT_KEY] = exec_http_extreme_vsp(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="openconfig-system:system",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_SYS_DICT_KEY])

    output_dict[FACTS_INT_DICT_KEY] = exec_http_extreme_vsp(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="openconfig-interfaces:interfaces",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(output_dict[FACTS_INT_DICT_KEY])

    task.host[FACTS_DATA_HOST_KEY] = _extreme_vsp_facts_api_converter(
        hostname=task.host.hostname,
        cmd_output=output_dict,
        options=options
    )


def _extreme_vsp_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "EXTREME_VSP-FACT NOT IMPLEMENTED"
    )


def _extreme_vsp_get_facts_ssh(task, options={}):
    raise NetestsFunctionNotImplemented(
        "EXTREME_VSP-FACT NOT IMPLEMENTED"
    )
