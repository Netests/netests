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
ERROR_HEADER = "Error import [ospf_converters.py]"
HEADER_GET = "[netests - ospf_converters]"

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
    from protocols.ospf import OSPFSession, ListOSPFSessions, OSPFSessionsArea, ListOSPFSessionsArea
    from protocols.ospf import OSPFSessionsVRF, ListOSPFSessionsVRF, OSPF
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ospf")
    exit(EXIT_FAILURE)
    print(importError)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Functions
#

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus Networks OSPF converter
#
def _cumulus_ospf_converter(hostname:str(), cmd_outputs:list) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(list())

    for cmd_output in cmd_outputs:

        if cmd_output.get('data', NOT_SET).get('neighbors', NOT_SET) is NOT_SET:
            ### VRF
            for vrf, ospf_facts in cmd_output.get('data', NOT_SET).items():
                vrf_name = vrf

            ospf_sessions_vrf = OSPFSessionsVRF(
                router_id=cmd_output.get('rid', NOT_SET).get(vrf_name, NOT_SET).get('routerId', NOT_SET),
                vrf_name=vrf_name,
                ospf_sessions_area_lst=ListOSPFSessionsArea(list())
            )

            result_area = dict()

            for neighbor_rid , neighbors_facts in cmd_output.get('data', NOT_SET).get(
                    vrf_name, NOT_SET).get('neighbors', NOT_SET).items():

                ospf = OSPFSession(
                    hostname=hostname,
                    peer_rid=neighbor_rid,
                    peer_hostname=NOT_SET,
                    session_state=neighbors_facts[0].get('nbrState', NOT_SET),
                    local_interface=_mapping_interface_name(neighbors_facts[0].get('ifaceName', NOT_SET)),
                    peer_ip=neighbors_facts[0].get('ifaceAddress', NOT_SET),
                )

                if neighbors_facts[0].get('areaId', NOT_SET) not in result_area.keys():
                    result_area[neighbors_facts[0].get('areaId', NOT_SET)] = OSPFSessionsArea(
                        area_number=neighbors_facts[0].get('areaId', NOT_SET),
                        ospf_sessions=ListOSPFSessions(list())
                    )

                result_area.get(neighbors_facts[0].get('areaId', NOT_SET)).ospf_sessions.ospf_sessions_lst.append(ospf)

                for area_id, ospf_sessions in result_area.items():
                    ospf_sessions_vrf.ospf_sessions_area_lst.ospf_sessions_area_lst.append(ospf_sessions)

        else:

            ospf_sessions_vrf = OSPFSessionsVRF(
                router_id=cmd_output.get('rid', NOT_SET).get('routerId', NOT_SET),
                vrf_name="default",
                ospf_sessions_area_lst=ListOSPFSessionsArea(list())
            )

            result_area = dict()

            for neighbor_rid, neighbors_facts in cmd_output.get('data', NOT_SET).get('neighbors', NOT_SET).items():

                ospf = OSPFSession(
                    hostname=hostname,
                    peer_rid=neighbor_rid,
                    peer_hostname=NOT_SET,
                    session_state=neighbors_facts[0].get('nbrState', NOT_SET),
                    local_interface=_mapping_interface_name(neighbors_facts[0].get('ifaceName', NOT_SET)),
                    peer_ip=neighbors_facts[0].get('ifaceAddress', NOT_SET),
                )

                if neighbors_facts[0].get('areaId', NOT_SET) not in result_area.keys():
                    result_area[neighbors_facts[0].get('areaId', NOT_SET)] = OSPFSessionsArea (
                        area_number=neighbors_facts[0].get('areaId', NOT_SET),
                        ospf_sessions=ListOSPFSessions(list())
                    )

                result_area.get(neighbors_facts[0].get('areaId', NOT_SET)).ospf_sessions.ospf_sessions_lst.append(ospf)


            for area_id, ospf_sessions in result_area.items():
                ospf_sessions_vrf.ospf_sessions_area_lst.ospf_sessions_area_lst.append(ospf_sessions)


        ospf_vrf_lst.ospf_sessions_vrf_lst.append(ospf_sessions_vrf)

    return  OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus OSPF Converter
#
def _nexus_ospf_converter(hostname:str(), cmd_outputs:list) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(list())

    for cmd_output in cmd_outputs:

        ospf_sessions_vrf = OSPFSessionsVRF(
            router_id=cmd_output.get('rid').get('TABLE_ctx').get('ROW_ctx')[0].get('rid', NOT_SET),
            vrf_name=cmd_output.get('rid').get('TABLE_ctx').get('ROW_ctx')[0].get('cname', NOT_SET),
            ospf_sessions_area_lst=ListOSPFSessionsArea(list())
        )

        session_by_area = dict()

        for session in cmd_output.get('data').get('TABLE_ctx').get('ROW_ctx').get('TABLE_nbr').get('ROW_nbr'):

            ospf = OSPFSession(
                hostname=hostname,
                peer_rid=session.get('rid', NOT_SET),
                peer_hostname=NOT_SET,
                session_state=session.get('state', NOT_SET),
                local_interface=_mapping_interface_name(session.get('intf', NOT_SET)),
                peer_ip=session.get('addr', NOT_SET)
            )

            if session.get('area') not in session_by_area.keys():
                session_by_area[session.get('area')] = list()

            session_by_area[session.get('area')].append(ospf)

        for area_id, sessions in session_by_area.items():

            ospf_sessions_vrf.ospf_sessions_area_lst.ospf_sessions_area_lst.append(
                OSPFSessionsArea(
                    area_number=area_id,
                    ospf_sessions=ListOSPFSessions(
                        ospf_sessions_lst=sessions
                    )
                )
            )

        ospf_vrf_lst.ospf_sessions_vrf_lst.append(ospf_sessions_vrf)

    return  OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista OSPF Converter
#
def _arista_ospf_converter(hostname:str(), cmd_outputs:list) -> OSPF:
    pass