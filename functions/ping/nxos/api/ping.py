#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_rpc_nxos
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
from const.constants import NOT_SET, LEVEL5, JINJA2_PING_RESULT
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_ping_api_exec(task, options={}):
    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
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

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL5
        ):
            printline()
            PP.pprint(o)

        _raise_exception_on_ping_cmd(
            output=o.get('result').get('msg'),
            hostname=task.host.name,
            ping_line=ping_line,
            must_work=must_works
        )
