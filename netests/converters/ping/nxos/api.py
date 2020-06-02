#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests import log
from nornir.core.task import Result
from netests.constants import JINJA2_PING_RESULT
from netests.tools.http import exec_http_rpc_nxos
from netests.converters.ping.ping_validator import _raise_exception_on_ping_cmd


def _nxos_ping_api_exec(task):
    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
    result = True
    for ping_line in file:
        if "!" in ping_line and "PING NOT AVAILABLE" not in ping_line:
            ping_line = ping_line.replace("!", "")
            must_works = False
        else:
            must_works = True

        o = exec_http_rpc_nxos(
            hostname=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            command=ping_line,
            secure_api=task.host.get('secure_api', False)
        )

        if not isinstance(o, dict):
            o = json.loads(o)

        log.debug(
            "\n"
            "Execute the following ping command on NXOS API\n"
            f"{ping_line}"
            "Result is :\n"
            f"{o}"
        )

        r = _raise_exception_on_ping_cmd(
            output=o.get('result').get('msg'),
            hostname=task.host.name,
            platform=task.host.platform,
            connexion=task.host.get('connexion', 'host'),
            ping_line=ping_line,
            must_work=must_works
        )

        if r is False:
            result = False

    return Result(host=task.host, result=result)
