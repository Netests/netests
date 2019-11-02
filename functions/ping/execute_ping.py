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
    # To use advanced filters
    from nornir.core.filter import F
    # To generate template with Jinja2
    from nornir.plugins.tasks.text import template_file
    # To print task results
    from nornir.plugins.functions.text import print_result
    # To execute remote command on devices
    from nornir.plugins.tasks.commands import remote_command
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
        num_workers=1
    )
    print_result(data_retrieve)

    generate_cmd = devices.run(
        task=_generic_generate_ping_cmd,
        on_failed=True,
        num_workers=10
    )
    print_result(generate_cmd)

    execute_cmd = devices.run(
        task=_execute_ping_cmd,
        on_failed=True,
        num_workers=10
    )
    print_result(execute_cmd)

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

    file = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "r")

    for ping_line in file:
        try:
            output = task.run(
                name=f"Ping network devices",
                task=remote_command,
                command=ping_line
            )
            #print_result(output)

        except Exception as identifier:
            print(f"[PINGS] ERROR WITH {task.host} _> {ping_line}")
