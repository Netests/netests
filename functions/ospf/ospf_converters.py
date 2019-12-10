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

    ospf_vrf_lst = ListOSPFSessionsVRF(
        list()
    )
    router_id = ""
    inst = ""
    vrf = ""

    for cmd_output in cmd_outputs:

        if 'vrfs' in cmd_output.get('rid').keys():

            # Retrieve router ID from "show ip ospf | json"
            for vrf_name in cmd_output.get('rid').get('vrfs').keys():
                for instance, facts in cmd_output.get('rid').get('vrfs').get(vrf_name).get('instList').items():
                    router_id = facts.get('routerId', NOT_SET)
                    inst = instance
                    vrf = vrf_name

            ospf_sessions_vrf = OSPFSessionsVRF(
                router_id=router_id,
                vrf_name=vrf,
                ospf_sessions_area_lst=ListOSPFSessionsArea(list())
            )

            session_by_area = dict()

            for adj in cmd_output.get('data').get('vrfs').get(vrf).get('instList').get(inst).get('ospfNeighborEntries'):

                ospf = OSPFSession(
                    hostname=hostname,
                    peer_rid=adj.get('routerId', NOT_SET),
                    peer_hostname=NOT_SET,
                    session_state=adj.get('adjacencyState', NOT_SET),
                    local_interface=_mapping_interface_name(adj.get('interfaceName', NOT_SET)),
                    peer_ip=adj.get('interfaceAddress', NOT_SET)
                )

                if adj.get('details').get('areaId') not in session_by_area.keys():
                    session_by_area[adj.get('details').get('areaId')] = list()

                session_by_area[adj.get('details').get('areaId')].append(ospf)

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

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Network VSP OSPF Converter
#
def _extreme_vsp_ospf_converter(hostname:str(), cmd_outputs:json) -> OSPF:

    if cmd_outputs is None:
        return None

    ospf_vrf_lst = ListOSPFSessionsVRF(
        list()
    )

    formated_data = _extreme_vsp_format_data(
        cmd_outputs=cmd_outputs
    )

    for vrf in formated_data:

        ospf_area_lst = ListOSPFSessionsArea(
            ospf_sessions_area_lst=list()
        )

        for area in formated_data.get(vrf):

            ospf_session_lst = ListOSPFSessions(
                ospf_sessions_lst=list()
            )

            for interface in formated_data.get(vrf).get(area):

                ospf_session_lst.ospf_sessions_lst.append(
                    OSPFSession(
                        hostname=hostname,
                        peer_rid=formated_data.get(vrf).get(area).get(interface).get('peer_rid', NOT_SET),
                        peer_hostname=NOT_SET,
                        session_state=formated_data.get(vrf).get(area).get(interface).get('session_state', NOT_SET),
                        local_interface=NOT_SET,
                        peer_ip=formated_data.get(vrf).get(area).get(interface).get('peer_ip', NOT_SET)
                    )
                )

            ospf_area_lst.ospf_sessions_area_lst.append(
                OSPFSessionsArea(
                    area_number=area,
                    ospf_sessions=ospf_session_lst
                )
            )

        ospf_vrf_lst.ospf_sessions_vrf_lst.append(
            OSPFSessionsVRF(
                vrf_name=vrf,
                router_id=cmd_outputs.get(vrf).get(OSPF_RIB_KEY)[0][0],
                ospf_sessions_area_lst=ospf_area_lst
            )
        )

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Extreme Network VSP OSPF data Formater
#
def _extreme_vsp_format_data(cmd_outputs:json) -> json:

    result = dict()
    temp_result = dict()

    for vrf in cmd_outputs:

        result[vrf] = dict()
        temp_result[vrf] = dict()

        if OSPF_NEI_KEY in cmd_outputs.get(vrf):
            for neighbors in cmd_outputs.get(vrf).get(OSPF_NEI_KEY):

                temp_result[vrf][neighbors[0]] = dict()

                temp_result[vrf][neighbors[0]]['peer_rid'] = neighbors[1]
                temp_result[vrf][neighbors[0]]['peer_ip'] = neighbors[2]
                temp_result[vrf][neighbors[0]]['session_state'] = neighbors[4]


        if OSPF_INT_KEY in cmd_outputs.get(vrf):
            for neighbors_int in cmd_outputs.get(vrf).get(OSPF_INT_KEY):

                if neighbors_int[0] in temp_result[vrf].keys():

                    if neighbors_int[1] not in result[vrf].keys():
                        result[vrf][neighbors_int[1]] = dict()

                    result[vrf][neighbors_int[1]][neighbors_int[0]] = temp_result[vrf][neighbors_int[0]]

    return result
