#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Add a description ....

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [vrf_gets.py]"
HEADER_GET = "[netests - vrf_gets]"
########################################################################################################################
#
# Import Library
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from protocols.ping import PING
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.ping.retrieve_ping import retrieve_ping_from_yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from nornir.core import Nornir
    from nornir.core.task import MultiResult
    from nornir.core.task import AggregatedResult
    # To use advanced filters
    from nornir.core.filter import F
    # To generate template with Jinja2
    from nornir.plugins.tasks.text import template_file
    # To print task results
    from nornir.plugins.functions.text import print_result
    # To execute remote command on devices
    from nornir.plugins.tasks.commands import remote_command
    # To raise an Nornir Exception
    from nornir.core.exceptions import NornirExecutionError
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import os
except ImportError as importError:
    print(f"{ERROR_HEADER} os")
    exit(EXIT_FAILURE)
    print(importError)


########################################################################################################################
#
# Functions
#
def execute_ping(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    path_url = f"{PATH_TO_VERITY_FILES}{PING_SRC_FILENAME}"

    data_retrieve = devices.run(
        task=retrieve_ping_from_yaml,
        on_failed=True,
        num_workers=10
    )
    #print_result(data_retrieve)

    generate_cmd = devices.run(
        task=_generic_generate_ping_cmd,
        on_failed=True,
        num_workers=10
    )
    #print_result(generate_cmd)

    execute_cmd = devices.run(
        task=_execute_ping_cmd,
        on_failed=True,
        num_workers=10
    )
    #print_result(execute_cmd)

    return (not execute_cmd.failed)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic functions
#
def _generic_generate_ping_cmd(task):

    data = task.run(
        name="Generate Cumulus interfaces configuration",
        task=template_file,
        template=f"{task.host.platform}_ping.j2",
        path=f"{JINJA2_PING_PATH}/",
    )

    # Create folder templates/
    if not os.path.exists(TEMPLATES_PATH):
        os.makedirs(TEMPLATES_PATH)

    # Create folder templates/jinja2/
    if not os.path.exists(JINJA2_PATH):
        os.makedirs(JINJA2_PATH)

    # Create folder templates/jinja2/ping/
    if not os.path.exists(JINJA2_PING_PATH):
        os.makedirs(JINJA2_PING_PATH)

    # Create folder templates/jinja2/ping/result
    if not os.path.exists(JINJA2_PING_RESULT):
        os.makedirs(JINJA2_PING_RESULT)

    f = open(
        f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "w+")
    f.write(data.result)
    f.close()


# ----------------------------------------------------------------------------------------------------------------------
#
# Execute ping command
#
def _execute_ping_cmd(task):

    if task.host.platform == ARISTA_PLATEFORM_NAME:
        _execute_generic_ping_cmd(task, enable=True)

    else:
        # Ok for Cumulus & Cisco Nexus
        _execute_generic_ping_cmd(task)


# ----------------------------------------------------------------------------------------------------------------------
#
# Execute ping commands on Arista Networks
#
def _execute_arista_ping_cmd(task):

    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")

    for ping_line in file:

        output = task.run(
            name=f"Ping network devices",
            task=remote_command,
            command=f"enable \n {ping_line}"
        )
        # print_result(output)

        _raise_exception_on_ping_cmd(output.result, task.host.name, ping_line)

# ----------------------------------------------------------------------------------------------------------------------
#
# Execute ping commands on Generice devices
#
def _execute_generic_ping_cmd(task, *, enable=False):

    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")
    must_works = True

    for ping_line in file:

        if enable:
            ping_line = "enable \n " + ping_line

        if "!" in ping_line and "PING NOT AVAILABLE" not in ping_line:
            ping_line = ping_line.replace("!", "")
            must_works = False
        else:
            must_works = True

        output = task.run(
            name=f"Ping network devices",
            task=remote_command,
            command=f"{ping_line}"
        )
        # print_result(output)

        if task.host.platform != CUMULUS_PLATEFORM_NAME:
            _raise_exception_on_ping_cmd(output, task.host.name, ping_line, must_works)

# ----------------------------------------------------------------------------------------------------------------------
#
# Raise a exception if output is not
#
def _raise_exception_on_ping_cmd(output:MultiResult, hostname:str, ping_line:str, must_work:bool) -> None :

    if must_work:
        if "Invalid host/interface " in output.result or \
                "Network is unreachable" in output.result or \
                "Temporary failure in name resolution" in output.result or \
                "100% packet loss" in output.result or \
                "0 received" in output.result:

            print(f"[PINGS] ERROR WITH {hostname} _> {ping_line} = must_work={must_work}")
            raise Exception("ERROR")
    else:
        if ("1 packets received" in output.result and "0.00% packet loss" in output.result) or \
                ("1 received" in output.result and "0% packet loss" in output.result):
            print(f"[PINGS] ERROR WITH {hostname} _> {ping_line} = must_work={must_work}")
            raise Exception("ERROR")