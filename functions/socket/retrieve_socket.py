#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [retrieve_socket.py]"
HEADER_GET = "[netests - retrieve_socket]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from protocols.socket import SOCKET, ListSOCKET
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.socket")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.global_tools import open_file
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)


try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    print(importError)
    exit(EXIT_FAILURE)

# ----------------------------------------------------------------------------------------------------------------------
#
#
def retrieve_socket_from_yaml(task) -> list():
    """
    This function will retrieve all sockets to execute from the YAML.
    Given a host, this function will retrieve all ip_addr to socket in "all." / "groups"
    :param task: Nornir Task
    :return list: IP_ADDR to socket
    """

    socket_lst = ListSOCKET(
        list()
    )
    socket_data = open_file(f"{PATH_TO_VERITY_FILES}{SOCKET_SRC_FILENAME}")

    # Retrieve data in "all:"
    if YAML_ALL_GROUPS_KEY in socket_data.keys():
        for socket in socket_data.get(YAML_ALL_GROUPS_KEY, NOT_SET):

            socket_obj = SOCKET(
                ip=socket.get('ip', NOT_SET),
                port=socket.get('port', NOT_SET),
                timeout=socket.get('timeout', 1),
                vrf=socket.get('vrf', "default"),
                protocol=socket.get('protocol', "tcp"),
                work=socket.get('work', True)
            )

            socket_lst.socket_lst.append(socket_obj)


    # Retrieve data in "groups:"
    if YAML_GROUPS_KEY in socket_data.keys():
        for value_key_groups in socket_data.get(YAML_GROUPS_KEY, NOT_SET).keys():
            for host_group in task.host.groups:
                if "," in value_key_groups:
                    if host_group in value_key_groups.split(","):
                        for socket in socket_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            socket_obj = SOCKET(
                                ip=socket.get('ip', NOT_SET),
                                port=socket.get('port', NOT_SET),
                                timeout=socket.get('timeout', 1),
                                vrf=socket.get('vrf', "default"),
                                protocol=socket.get('protocol', "tcp"),
                                work=socket.get('work', True)
                            )

                            socket_lst.socket_lst.append(socket_obj)

                else:
                    if host_group == value_key_groups:
                        for socket in socket_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            socket_obj = SOCKET(
                                ip=socket.get('ip', NOT_SET),
                                port=socket.get('port', NOT_SET),
                                timeout=socket.get('timeout', 1),
                                vrf=socket.get('vrf', "default"),
                                protocol=socket.get('protocol', "tcp"),
                                work=socket.get('work', True)
                            )

                            socket_lst.socket_lst.append(socket_obj)


    # Retrieve data in "devices:"
    if YAML_DEVICES_KEY in socket_data.keys():
        for value_key_devices in socket_data.get(YAML_DEVICES_KEY, NOT_SET).keys():
            if "," in value_key_devices:
                if task.host.name in value_key_devices.split(","):
                    for socket in socket_data.get(YAML_DEVICES_KEY, NOT_SET).get(value_key_devices, NOT_SET):

                        socket_obj = SOCKET(
                            ip=socket.get('ip', NOT_SET),
                            port=socket.get('port', NOT_SET),
                            timeout=socket.get('timeout', 1),
                            vrf=socket.get('vrf', "default"),
                            protocol=socket.get('protocol', "tcp"),
                            work=socket.get('work', True)
                        )

                        socket_lst.socket_lst.append(socket_obj)

            else:
                if task.host.name == value_key_devices:

                    for socket in socket_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_devices):

                        socket_obj = SOCKET(
                            ip=socket.get('ip', NOT_SET),
                            port=socket.get('port', NOT_SET),
                            timeout=socket.get('timeout', 1),
                            vrf=socket.get('vrf', "default"),
                            protocol=socket.get('protocol', "tcp"),
                            work=socket.get('work', True)
                        )

                        socket_lst.socket_lst.append(socket_obj)


    # Retrieve data per device
    if task.host.name in socket_data.keys():

        for socket in socket_data.get(task.host.name, NOT_SET):

            socket_obj = SOCKET(
                ip=socket.get('ip', NOT_SET),
                port=socket.get('port', NOT_SET),
                timeout=socket.get('timeout', 1),
                vrf=socket.get('vrf', "default"),
                protocol=socket.get('protocol', "tcp"),
                work=socket.get('work', True)
            )

            socket_lst.socket_lst.append(socket_obj)

    task.host[SOCKET_DATA_HOST_KEY] = socket_lst