#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from functions.http_request import exec_http_call_juniper
from const.constants import NOT_SET, LEVEL5, PING_DATA_HOST_KEY
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_ping_api_exec(task, options={}):
    for ping_line in task.host[PING_DATA_HOST_KEY].ping_lst:
        o = exec_http_call_juniper(
            hostname=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            endpoint=(
                "ping?count=1"
                "&wait=1"
                f"&host={ping_line.ip_address}"
                f"&routing-instance={ping_line.vrf}"
            ),
            secure_api=task.host.get('secure_api', False)
        )

        o = format_xml_output(o)

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL5
        ):
            printline()
            PP.pprint(o)
            PP.pprint(ping_line.to_json())

        if 'ping-results' in o.keys():
            _raise_exception_on_ping_cmd(
                output=o,
                hostname=task.host.name,
                platform=task.host.platform,
                connexion=task.host.get('connexion'),
                ping_line=ping_line,
                must_work=ping_line.works
            )
