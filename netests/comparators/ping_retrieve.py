#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.plugins.tasks.text import template_file
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.protocols.ping import PING, ListPING
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)
from netests.constants import (
    NOT_SET,
    PING_DATA_HOST_KEY,
    TEMPLATES_PATH,
    JINJA2_PATH,
    JINJA2_PING_PATH,
    JINJA2_PING_RESULT
)


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
                    vrf=p.get('vrf', "default"),
                    works=p.get('works', True),
                )
            )

    task.host[PING_DATA_HOST_KEY] = ping_lst


def _generic_generate_ping_cmd(task):

    data = task.run(
        name="Generate CLI command to execute ping.",
        task=template_file,
        template=f"{task.host.platform}_ping.j2",
        path=f"{JINJA2_PING_PATH}/",
    )

    # Create folder templates/
    if not os.path.exists(TEMPLATES_PATH):
        os.makedirs(TEMPLATES_PATH)

    # Create folder templates/jinja2/
    if not os.path.exists(JINJA2_PATH):
        os.makedirs(JINJA2_PATH)

    # Create folder templates/jinja2/ping/
    if not os.path.exists(JINJA2_PING_PATH):
        os.makedirs(JINJA2_PING_PATH)

    # Create folder templates/jinja2/ping/result
    if not os.path.exists(JINJA2_PING_RESULT):
        os.makedirs(JINJA2_PING_RESULT)

    f = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "w+")
    f.write(data.result)
    f.close()
