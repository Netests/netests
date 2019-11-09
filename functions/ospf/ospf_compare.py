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
ERROR_HEADER = "Error import [ospf_compare.py]"
HEADER_GET = "[netests - compare_ospf]"

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
    from protocols.ospf import OSPFSession, ListOSPFSessions, OSPFSessionsArea, ListOSPFSessionsArea
    from protocols.ospf import OSPFSessionsVRF, ListOSPFSessionsVRF, OSPF
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ospf")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def compare_ospf(nr, ospf_data:json, level_test:int) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_ospf,
        ospf_data=ospf_data,
        level_test=level_test,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(f"{HEADER_GET} Task '_compare' has failed for {value.host} (value.result={value.result}).")
            return_value = False

    return (not data.failed and return_value)

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_ospf(task, ospf_data:json, level_test:int):

    ospf_sessions_vrf_lst = ListOSPFSessionsVRF(list())

    if OSPF_SESSIONS_HOST_KEY in task.host.keys():

        for vrf_name, ospf_vrf_facts in ospf_data.get(task.host.name, NOT_SET).items():

            ospf_sessions_vrf = OSPFSessionsVRF(
                router_id=ospf_vrf_facts.get('router_id', NOT_SET),
                vrf_name=vrf_name,
                ospf_sessions_area_lst=ListOSPFSessionsArea(list())
            )

            for area_id, session_in_area in ospf_vrf_facts.get('area_id', NOT_SET).items():

                ospf_session_area = OSPFSessionsArea(
                    area_number=area_id,
                    ospf_sessions=ListOSPFSessions(list())
                )

                for neighbor in session_in_area:

                    if isinstance(neighbor,dict):

                        ospf = OSPFSession(
                            hostname=task.host.name,
                            peer_rid=neighbor.get('peer_rid', NOT_SET),
                            peer_hostname=neighbor.get('peer_name', NOT_SET),
                            session_state=neighbor.get('state', NOT_SET),
                            local_interface=neighbor.get('local_interface', NOT_SET),
                            peer_ip=neighbor.get('peer_ip', NOT_SET),
                        )

                        ospf_session_area.ospf_sessions.ospf_sessions_lst.append(ospf)

                ospf_sessions_vrf.ospf_sessions_area_lst.ospf_sessions_area_lst.append(ospf_session_area)

            ospf_sessions_vrf_lst.ospf_sessions_vrf_lst.append(ospf_sessions_vrf)

        verity_ospf = OSPF(
            hostname=task.host.name,
            ospf_sessions_vrf_lst=ospf_sessions_vrf_lst
        )


        is_same = verity_ospf == task.host[OSPF_SESSIONS_HOST_KEY]

        task.host[OSPF_WORKS_KEY] = is_same
        return is_same

    else:
        print(f"Key {OSPF_SESSIONS_HOST_KEY} is missing for {task.host.name}")

