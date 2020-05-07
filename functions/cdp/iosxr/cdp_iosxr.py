#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import NOT_SET, LEVEL2, IOSXR_GET_CDP, CDP_DATA_HOST_KEY
from functions.cdp.iosxr.ssh.converter import _iosxr_cdp_ssh_converter


def _iosxr_get_cdp_api(task, options={}):
    pass


def _iosxr_get_cdp_netconf(task):
    pass


def _iosxr_get_cdp_ssh(task, options={}):
    output = task.run(
        name=f"{IOSXR_GET_CDP}",
        task=netmiko_send_command,
        command_string=IOSXR_GET_CDP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    task.host[CDP_DATA_HOST_KEY] = _iosxr_cdp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output.result,
        options=options
    )
