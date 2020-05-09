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
            PP.pprint(p.to_json())

        arista_api_validate_output(
            output=output,
            hostname=task.host.name,
            platform=task.host.platform,
            ping_print=p.to_json(),
            ping_works=p.works,
        )


def arista_api_validate_output(
    output: dict,
    hostname: str,
    platform: str,
    ping_print: str,
    ping_works: bool
) -> None:
    if isinstance(output, dict) and 'result' in output.keys():
        for d in output.get('result'):
            if 'messages' in d.keys():
                _raise_exception_on_ping_cmd(
                    output=d.get('messages')[0],
                    hostname=hostname,
                    platform=platform,
                    ping_line=ping_print,
                    must_work=ping_works
                )
