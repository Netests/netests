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
ERROR_HEADER = "Error import [execute_socket.py]"
HEADER_GET = "[netests - execute_socket]"
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
    from protocols.socket import SOCKET
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.socket")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.socket.retrieve_socket import retrieve_socket_from_yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.socket.retrieve_socket")
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
    from nornir.plugins.tasks.networking import netmiko_send_command
    # To raise an Nornir Exception
    from nornir.core.exceptions import NornirExecutionError, CommandError
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
def execute_socket(nr: Nornir):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    path_url = f"{PATH_TO_VERITY_FILES}{SOCKET_SRC_FILENAME}"

    data_retrieve = devices.run(
        task=retrieve_socket_from_yaml,
        on_failed=True,
        num_workers=10
    )
    #print_result(data_retrieve)

    generate_cmd = devices.run(
        task=_generic_generate_socket_cmd,
        on_failed=True,
        num_workers=10
    )
    #print_result(generate_cmd)

    execute_cmd = devices.run(
        task=_execute_socket_cmd,
        on_failed=True,
        num_workers=10
    )
    #print_result(execute_cmd)

    return (not execute_cmd.failed)

# ----------------------------------------------------------------------------------------------------------------------
#
# Generic functions
#
def _generic_generate_socket_cmd(task):

    data = task.run(
        name="Generate socket commands",
        task=template_file,
        template=f"{task.host.platform}_socket.j2",
        path=f"{JINJA2_SOCKET_PATH}/",
    )

    # Create folder templates/
    if not os.path.exists(TEMPLATES_PATH):
        os.makedirs(TEMPLATES_PATH)

    # Create folder templates/jinja2/
    if not os.path.exists(JINJA2_PATH):
        os.makedirs(JINJA2_PATH)

    # Create folder templates/jinja2/socket/
    if not os.path.exists(JINJA2_SOCKET_PATH):
        os.makedirs(JINJA2_SOCKET_PATH)

    # Create folder templates/jinja2/socket/result
    if not os.path.exists(JINJA2_SOCKET_RESULT):
        os.makedirs(JINJA2_SOCKET_RESULT)

    f = open(
        f"{JINJA2_SOCKET_RESULT}{task.host.name}_socket_cmd", "w+")
    f.write(data.result)
    f.close()


# ----------------------------------------------------------------------------------------------------------------------
#
# Execute socket command
#
def _execute_socket_cmd(task):

    if task.host.platform == CUMULUS_PLATEFORM_NAME:
        _execute_generic_socket_cmd(
            task,
            use_netmiko=False,
            enable=False
        )

    else:
        print(f"{HEADER_GET} Socket is not implemented for {task.host.platform}")

# ----------------------------------------------------------------------------------------------------------------------
#
# Execute Socket commands on Generice devices
#
def _execute_generic_socket_cmd(task, *, use_netmiko=False, enable=False):

    file = open(f"{JINJA2_SOCKET_RESULT}{task.host.name}_socket_cmd", "r")
    error = False

    for socket_line in file:
        try:

            output = task.run(
                name=f"Execute socket test",
                task=remote_command,
                command=f"{socket_line}"
            )
            #print_result(output)

        except Exception as e:
            print(f"{HEADER_GET} Error with {task.host.name} with the command _> {socket_line}")
            error = True

    if error:
        print(f"{HEADER_GET} Netcat is not installed on the device. Please install nc [sudo apt install netcat]")