#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.commands import remote_command
from const.constants import NOT_SET, LEVEL4, PING_DATA_HOST_KEY
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _arista_ping_ssh_exec(task, options={}):
    for ping_line in task.host[PING_DATA_HOST_KEY]:
        data = task.run(
            name=f"Execute {ping_line}",
            task=remote_command,
            command=f"enable \n {ping_line}"
        )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL4
        ):
            print_result(data)

        _raise_exception_on_ping_cmd(
            data.result,
            task.host.name,
            ping_line)
