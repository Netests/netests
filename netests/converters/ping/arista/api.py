#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyeapi
from netests import log
from nornir.core.task import Result
from netests.constants import PING_DATA_HOST_KEY
from netests.converters.ping.ping_validator import _raise_exception_on_ping_cmd


def _arista_ping_api_exec(task):
    c = pyeapi.connect(
        transport=task.host.get('secure_api', 'https'),
        host=task.host.hostname,
        username=task.host.username,
        password=task.host.password,
        port=task.host.port
    )

    result = True
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

        log.debug(
            "\n"
            "Execute the following ping command on Arista API\n"
            "[ "
            "enable , ",
            f"ping vrf {p.vrf} {p.ip_address} repeat 1 timeout 2 ]"
            "From the following PING object :\n"
            f"{p.to_json()}"
            "Result is :\n"
            f"{output}"
        )

        r = arista_api_validate_output(
            output=output,
            hostname=task.host.name,
            platform=task.host.platform,
            connexion=task.host.get('connexion', 'ssh'),
            ping_print=p.to_json(),
            ping_works=p.works,
        )

        if r is False:
            result = False

    return Result(host=task.host, result=result)


def arista_api_validate_output(
    output: dict,
    hostname: str,
    platform: str,
    connexion: str,
    ping_print: str,
    ping_works: bool
) -> None:
    if isinstance(output, dict) and 'result' in output.keys():
        for d in output.get('result'):
            if 'messages' in d.keys():
                return _raise_exception_on_ping_cmd(
                    output=d.get('messages')[0],
                    hostname=hostname,
                    platform=platform,
                    connexion=connexion,
                    ping_line=ping_print,
                    must_work=ping_works
                )
