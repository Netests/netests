#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import pyeapi
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import NOT_SET, LEVEL5, PING_DATA_HOST_KEY
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_ping_api_exec(task, options={}):
    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )

    for p in task.host[PING_DATA_HOST_KEY].ping_lst:
        try:
            output = c.execute(
                [
                    "enable",
                    f"ping vrf {p.vrf} {p.ip_address} repeat 1 timeout 2"
                ]
            )
        except Exception:
            pass

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL5
        ):
            printline()
            PP.pprint(output)

        if isinstance(output, dict) and 'result' in output.keys():
            for d in output.get('result'):
                if 'messages' in d.keys():
                    _raise_exception_on_ping_cmd(
                        output="\n".join(d.get('messages')),
                        hostname=task.host.name,
                        platform=task.host.platform,
                        ping_line=p,
                        must_work=p.works
                    )
