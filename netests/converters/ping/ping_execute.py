#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from nornir.core.task import Result
from netests.constants import JINJA2_PING_RESULT
from nornir.plugins.tasks.commands import remote_command
from nornir.plugins.tasks.networking import netmiko_send_command
from netests.converters.ping.ping_validator import _raise_exception_on_ping_cmd


def _execute_netmiko_ping_cmd(task):
    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
    result = True
    for ping_line in file:
        if "!" in ping_line and "PING NOT AVAILABLE" not in ping_line:
            ping_line = ping_line.replace("!", "")
            must_works = False
        else:
            must_works = True

        data = task.run(
            name="Ping network devices",
            task=netmiko_send_command,
            command_string=f"{ping_line}",
            enable=True
        )

        log.debug(
            "\n"
            "Execute the following ping command with Netmiko\n"
            f"{ping_line}"
            f"must_works={must_works}"
            "Result is :\n"
            f"{data.result}"
        )

        r = _raise_exception_on_ping_cmd(
            output=data.result,
            hostname=task.host.name,
            platform=task.host.platform,
            connexion=task.host.get('connexion', 'ssh'),
            ping_line=ping_line,
            must_work=must_works
        )

        if r is False:
            result = False

    return Result(host=task.host, result=result)


def _execute_linux_ping_cmd(task):
    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
    result = True
    for ping_line in file:
        if "!" in ping_line and "PING NOT AVAILABLE" not in ping_line:
            ping_line = ping_line.replace("!", "")
            must_works = False
        else:
            must_works = True

        try:
            data = task.run(
                name="Ping network devices",
                task=remote_command,
                command=f"{ping_line}",
            )
            log.debug(
                "\n"
                "Execute the following ping command with Remote Command\n"
                f"{ping_line}"
                f"must_works={must_works}\n"
                "Result is :\n"
                f"{data.result}"
            )

        except Exception:
            log.debug(
                "\n In Exception part !\n"
                "Execute the following ping command with Remote Command\n"
                f"{ping_line}"
                f"must_works={must_works}"
                "Result is :\n"
                f"{data.result}"
            )
            result = False

    return Result(host=task.host, result=result)
