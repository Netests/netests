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
ERROR_HEADER = "Error import [retrieve_ping.py]"
HEADER_GET = "[netests - retrieve_ping]"

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
    from protocols.ping import PING, ListPING
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ping")
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
def retrieve_ping_from_yaml(task) -> list():
    """
    This function will retrieve all pings to execute from the YAML.
    Given a host, this function will retrieve all ip_addr to ping in "all." / "groups"
    :param task: Nornir Task
    :return list: IP_ADDR to ping
    """

    ping_lst = ListPING(
        list()
    )
    ping_data = open_file(f"{PATH_TO_VERITY_FILES}{PING_SRC_FILENAME}")

    # Retrieve data in "all:"
    if YAML_ALL_GROUPS_KEY in ping_data.keys():
        for ping in ping_data.get(YAML_ALL_GROUPS_KEY, NOT_SET):

            ping_obj = PING(
                src_host=task.host.name,
                ip_address=ping.get('ip', NOT_SET),
                vrf=ping.get('vrf', "default")
            )

            ping_lst.ping_lst.append(ping_obj)


    # Retrieve data in "groups:"
    if YAML_GROUPS_KEY in ping_data.keys():
        for value_key_groups in ping_data.get(YAML_GROUPS_KEY, NOT_SET).keys():
            for host_group in task.host.groups:
                if "," in value_key_groups:
                    if host_group in value_key_groups.split(","):
                        for ping in ping_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            ping_obj = PING(
                                src_host=task.host.name,
                                ip_address=ping.get('ip', NOT_SET),
                                vrf=ping.get('vrf', "default")
                            )

                            ping_lst.ping_lst.append(ping_obj)

                else:
                    if host_group == value_key_groups:
                        for ping in ping_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_groups):

                            ping_obj = PING(
                                src_host=task.host.name,
                                ip_address=ping.get('ip', NOT_SET),
                                vrf=ping.get('vrf', "default")
                            )

                            ping_lst.ping_lst.append(ping_obj)


    # Retrieve data in "devices:"
    if YAML_DEVICES_KEY in ping_data.keys():
        for value_key_devices in ping_data.get(YAML_DEVICES_KEY, NOT_SET).keys():
            if "," in value_key_devices:
                if task.host.name in value_key_devices.split(","):
                    for ping in ping_data.get(YAML_DEVICES_KEY, NOT_SET).get(value_key_devices, NOT_SET):

                        ping_obj = PING(
                            src_host=task.host.name,
                            ip_address=ping.get('ip', NOT_SET),
                            vrf=ping.get('vrf', "default")
                        )

                        ping_lst.ping_lst.append(ping_obj)

            else:
                if task.host.name == value_key_devices:

                    for ping in ping_data.get(YAML_GROUPS_KEY, NOT_SET).get(value_key_devices):

                        ping_obj = PING(
                            src_host=task.host.name,
                            ip_address=ping.get('ip', NOT_SET),
                            vrf=ping.get('vrf', "default")
                        )

                        ping_lst.ping_lst.append(ping_obj)


    # Retrieve data per device
    if task.host.name in ping_data.keys():

        for ping in ping_data.get(task.host.name, NOT_SET):

            ping_obj = PING(
                src_host=task.host.name,
                ip_address=ping.get('ip', NOT_SET),
                vrf=ping.get('vrf', "default")
            )

            ping_lst.ping_lst.append(ping_obj)

    task.host[PING_DATA_HOST_KEY] = ping_lst