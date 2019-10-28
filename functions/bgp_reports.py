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
ERROR_HEADER = "Error import [bgp_reports.py]"
HEADER_GET = "[netests - bgp_reports]"

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
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import time
except ImportError as importError:
    print(f"{ERROR_HEADER} time")
    exit(EXIT_FAILURE)
    print(importError)

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
def create_reports(nr, bgp_data:json):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    today = time.strftime("%Y-%m-%d_%H:%M")

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    if not os.path.exists(f"{REPORT_FOLDER}{today}/"):
        os.makedirs(f"{REPORT_FOLDER}{today}/")

    data = devices.run(
        task=_create,
        bgp_data=bgp_data,
        today=today,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

    return (not data.failed)


def _create(task, bgp_data:json, today:str):

    data_yaml = dict()
    data_yaml[task.host.name] = dict()

    data_yaml[task.host.name]['works'] = task.host.get(BGP_WORKS_KEY, NOT_SET)

    data_yaml[task.host.name]['as_number'] = dict()
    data_yaml[task.host.name]['as_number']['should_be'] = bgp_data.get(task.host.name).get(YAML_BGKP_ASN_KEY, NOT_SET)
    data_yaml[task.host.name]['as_number']['current_is'] = task.host.get(BGP_SESSIONS_HOST_KEY).as_number

    data_yaml[task.host.name]['router_id'] = dict()
    data_yaml[task.host.name]['router_id']['should_be'] = bgp_data.get(task.host.name).get(YAML_BGKP_ASN_KEY,NOT_SET)
    data_yaml[task.host.name]['router_id']['current_is'] = task.host.get(BGP_SESSIONS_HOST_KEY).router_id

    data_yaml[task.host.name]['neighbors'] = list()

    for neighbor in task.host.get(BGP_SESSIONS_HOST_KEY).bgp_sessions.bgp_sessions:

        tmp_dict = dict()

        tmp_dict['src_hostname'] = neighbor.src_hostname
        tmp_dict['peer_ip'] = neighbor.peer_ip
        tmp_dict['remote_as'] = neighbor.remote_as
        tmp_dict['peer_hostname'] = neighbor.peer_hostname
        tmp_dict['session_state'] = neighbor.session_state
        tmp_dict['state_time'] = neighbor.state_time
        tmp_dict['prefix_received'] = neighbor.prefix_received

        data_yaml[task.host.name]['neighbors'].append(tmp_dict)

    with open(f"{REPORT_FOLDER}{today}/{task.host.name}.yml", "w+") as outfile:
        yaml.dump(data_yaml, outfile, default_flow_style=False)