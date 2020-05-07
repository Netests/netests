#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import yaml
from const.constants import *
from protocols.ping import PING, ListPING
from functions.global_tools import open_file
from functions.select_vars import select_host_vars
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported

HEADER = "[netests - retrieve_ping]"


def retrieve_ping_from_yaml(task, test=False, options={}) -> ListPING:
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            ping_yaml_data = open_file(
                path="tests/features/src/ping_tests.yml"
            ).get(task.host.name)
        else:
            ping_yaml_data = select_host_vars(
                hostname=task.host.name,
                groups=task.host.groups,
                protocol="ping"
            )
    
    ping_lst = ListPING(
        ping_lst=list()
    )

    if ping_yaml_data is not None:
        for p in ping_yaml_data:
            ping_lst.ping_lst.append(
                PING(
                    src_host=task.host.name,
                    ip_address=p.get('ip', NOT_SET),
                    vrf=p.get('vrf', "default")
                )
            )

    task.host[PING_DATA_HOST_KEY] = ping_lst