#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.commands import remote_command
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ping.juniper.netconf.ping import _juniper_ping_netconf_exec
from functions.ping.juniper.api.ping import _juniper_ping_api_exec
from functions.ping.nxos.api.ping import _nxos_ping_api_exec
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
from const.constants import (
    NOT_SET,
    LEVEL4,
    JINJA2_PING_RESULT,
    ARISTA_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME,
    PING_DATA_HOST_KEY,
    API_CONNECTION,
    NETCONF_CONNECTION,
    SSH_CONNECTION
)


HEADER = "[netests - execute_ping]"


def execute_ping(nr: Nornir, options={}, from_cli=False) -> bool:
    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_execute_ping_cmd,
        on_failed=True,
        from_cli=from_cli,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        print_result(data)

    return (not data.failed)


def _execute_ping_cmd(task, from_cli=False):

    if (
        task.host.platform == JUNOS_PLATEFORM_NAME and
        task.host.get('connexion') == NETCONF_CONNECTION
    ):
        _juniper_ping_netconf_exec(task)

    elif (
        task.host.platform == JUNOS_PLATEFORM_NAME and
        task.host.get('connexion') == API_CONNECTION
    ):
        _juniper_ping_api_exec(task)

    elif (
        task.host.platform == NEXUS_PLATEFORM_NAME and
        task.host.get('connexion') == API_CONNECTION
    ):
        _nxos_ping_api_exec(task)

    elif task.host.platform == ARISTA_PLATEFORM_NAME:
        _execute_generic_ping_cmd(
            task,
            use_netmiko=False,
            enable=True
        )

    elif (
        task.host.get('connexion') == SSH_CONNECTION and
        (
            task.host.platform == CISCO_IOS_PLATEFORM_NAME or
            task.host.platform == JUNOS_PLATEFORM_NAME or
            task.host.platform == EXTREME_PLATEFORM_NAME
        )
    ):
        _execute_generic_ping_cmd(
            task,
            use_netmiko=True,
            enable=False
        )

    elif (
        task.host.get('connexion') == SSH_CONNECTION and
        (
            task.host.platform == NEXUS_PLATEFORM_NAME or
            task.host.platform == CUMULUS_PLATEFORM_NAME
        )
    ):
        _execute_generic_ping_cmd(
            task,
            use_netmiko=False,
            enable=False
        )


def _execute_arista_ping_cmd(task):
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


def _execute_generic_ping_cmd(task, *, use_netmiko=False, enable=False):

    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
    for ping_line in file:
        if enable:
            ping_line = "enable \n " + ping_line

        if "!" in ping_line and "PING NOT AVAILABLE" not in ping_line:
            ping_line = ping_line.replace("!", "")
            must_works = False
        else:
            must_works = True

        if use_netmiko:
            # IOS devices don't support "task=remote_command"
            data = task.run(
                name="Ping network devices",
                task=netmiko_send_command,
                command_string=f"{ping_line}"
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL4
            ):
                print_result(data)

        else:
            data = task.run(
                name="Ping network devices",
                task=remote_command,
                command=f"{ping_line}"
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL4
            ):
                print_result(data)

        if task.host.platform != CUMULUS_PLATEFORM_NAME:
            _raise_exception_on_ping_cmd(
                output=data.result,
                hostname=task.host.name,
                ping_line=ping_line,
                must_work=must_works
            )


def _execute_napalm_ping_cmd(task, *, enable=False):
    raise NotImplementedError()
