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
ERROR_HEADER = "Error import [bgp_converters.py]"
HEADER_GET = "[netests - bgp_converters]"

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
    from protocols.bgp import BGPSession, ListBGPSessions, BGPSessionsVRF, ListBGPSessionsVRF, BGP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.bgp")
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
# Generic state converter
#
def _generic_state_converter(state:str) -> str:
    """
    This function will convert session state in a session state brief (UP or DOWN)
    Example : Idle => Down

    :param state:
    :return str: State brief
    """

    if state in BGP_STATE_UP_LIST or state == NOT_SET:
        return BGP_STATE_BRIEF_UP
    else:
        return BGP_STATE_BRIEF_DOWN

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM BGP sessions state converter
#
def _napalm_bgp_status_converter(status:str) -> str:
    """
    This function is used to standardize BGP sessions state.
    Napalm use is_up=True and is_enable=True to simplify BGP state.
    In this project we use "UP/DOWN".

    'is_enabled': True,
    'is_up': True,

    :param status:
    :return str: Standard name of BGP state
    """
    if str(status).upper() == "TRUE":
        return "UP"
    elif str(status).upper() == "FALSE":
        return "DOWN"
    else:
        return status

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM global vrf converter
#
def _napalm_bgp_vrf_converter(vrf_name:str) -> str:
    """
    This function is used to standardize Global routing table name (vrf_name).
    Napalm named this routing table "global". Other word is "global", "grt" or "default".
    In this project we use "default".

    :param vrf_name:
    :return str: Global/Default routing table name
    """

    if str(vrf_name).upper() == "GLOBAL" or str(vrf_name).upper() == "GRT":
        return "default"
    else:
        return vrf_name

# ----------------------------------------------------------------------------------------------------------------------
#
# NAPALM BGP converter
#
def _napalm_bgp_converter(hostname:str(), cmd_output:json) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    local_as = ""

    if 'get_bgp_neighbors' in cmd_output.keys():

        for vrf_name, vrf_facts in cmd_output.get('get_bgp_neighbors').items():

            bgp_sessions_lst = ListBGPSessions(list())

            for peer_ip, facts in vrf_facts.get('peers').items():

                bgp_obj = BGPSession(
                    src_hostname=hostname,
                    peer_ip=peer_ip,
                    peer_hostname=facts.get('hostname', NOT_SET),
                    remote_as=facts.get('remote_as', NOT_SET),
                    state_brief=_napalm_bgp_status_converter(facts.get('is_up', NOT_SET)),
                    session_state=facts.get('session_state', NOT_SET),
                    state_time=facts.get('uptime', NOT_SET),
                    prefix_received=facts.get('address_family').get('ipv4').get('received_prefixes')
                )

                local_as = facts.get('local_as', NOT_SET)

                bgp_sessions_lst.bgp_sessions.append(bgp_obj)

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=_napalm_bgp_vrf_converter(vrf_name),
                as_number=local_as,
                router_id=vrf_facts.get('router_id'),
                bgp_sessions=bgp_sessions_lst
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cumulus BGP converter
#
def _cumulus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    as_number = ""
    router_id = ""
    vrf_name = ""
    state_brief = ""

    for cmd_output in cmd_outputs:
        if "ipv4 unicast" in cmd_output.keys():
            if cmd_output.get('ipv4 unicast', NOT_SET) is NOT_SET:
                return None

            else:

                bgp_sessions_lst = ListBGPSessions(list())

                if cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', NOT_SET) == "default":

                    as_number = cmd_output.get('ipv4 unicast', NOT_SET).get('as', NOT_SET)
                    router_id = cmd_output.get('ipv4 unicast', NOT_SET).get('routerId', NOT_SET)
                    vrf_name = cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', NOT_SET)

                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('peers', list()).items() :

                        if facts.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                            state_brief = BGP_STATE_BRIEF_UP
                        else:
                            state_brief = BGP_STATE_BRIEF_DOWN

                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            state_brief=state_brief,
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

                else:

                    as_number = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('as', NOT_SET)
                    router_id = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('routerId', NOT_SET)
                    vrf_name = cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('vrfName',NOT_SET)

                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('peers', list()).items():

                        if facts.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                            state_brief = BGP_STATE_BRIEF_UP
                        else:
                            state_brief = BGP_STATE_BRIEF_DOWN

                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            state_brief=state_brief,
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

                bgp_session_vrf = BGPSessionsVRF(
                    vrf_name=vrf_name,
                    as_number=as_number,
                    router_id=router_id,
                    bgp_sessions=bgp_sessions_lst
                )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus BGP Converter
#
def _nexus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        if isinstance(cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                'ROW_neighbor', NOT_SET), list):
            for neighbor in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',
                    NOT_SET).get('ROW_neighbor', NOT_SET):

                if neighbor.get('state', NOT_SET) in BGP_STATE_UP_LIST:
                    state_brief = BGP_STATE_BRIEF_UP
                else:
                    state_brief = BGP_STATE_BRIEF_DOWN

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=neighbor.get('neighbor-id', NOT_SET),
                    peer_hostname=neighbor.get('interfaces', NOT_SET),
                    remote_as=neighbor.get('remoteas', NOT_SET),
                    state_brief=state_brief,
                    session_state=neighbor.get('state', NOT_SET),
                    state_time=neighbor.get('LastUpDn', NOT_SET),
                    prefix_received=neighbor.get('prefixReceived', NOT_SET)
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

        elif isinstance(cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                'ROW_neighbor', NOT_SET), dict):

            if cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                    'ROW_neighbor', NOT_SET).get('state', NOT_SET) in BGP_STATE_UP_LIST:
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('neighbor-id', NOT_SET),
                peer_hostname=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('interfaces', NOT_SET),
                remote_as=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('remoteas', NOT_SET),
                state_brief=state_brief,
                session_state=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('state', NOT_SET),
                state_time=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor',NOT_SET).get('LastUpDn', NOT_SET),
                prefix_received=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor',NOT_SET).get('ROW_neighbor', NOT_SET).get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('vrf-name-out', NOT_SET),
            as_number=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('local-as', NOT_SET),
            router_id=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('router-id', NOT_SET),
            bgp_sessions=bgp_sessions_lst
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco IOS BGP Converter
#
def _ios_bgp_converter(hostname:str(), cmd_outputs:dict) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    for vrf in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(
            list()
        )

        for bgp_session in cmd_outputs.get(vrf):

            state_brief = BGP_STATE_BRIEF_UP
            asn = bgp_session[1]
            rid = bgp_session[0]

            if str(bgp_session[5]).isdigit() is False:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_sessions_lst.bgp_sessions.append(
                BGPSession(
                    src_hostname=hostname,
                    peer_ip=bgp_session[2],
                    peer_hostname=NOT_SET,
                    remote_as=bgp_session[3],
                    state_brief=state_brief,
                    session_state=bgp_session[5],
                    state_time=bgp_session[4],
                    prefix_received=NOT_SET
                )
            )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
            BGPSessionsVRF(
                vrf_name=vrf,
                as_number=asn,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst
            )
        )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Arista BGP Converter
#
def _arista_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )
    state_brief = ""

    for cmd_output in cmd_outputs:

        bgp_sessions_lst = ListBGPSessions(list())

        temp_value = cmd_output.get('vrfs', NOT_SET).keys()
        for key in temp_value:
            vrf_name = key
            break

        for neighbor, facts in cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('peers', NOT_SET).items():

            if facts.get('peerState', NOT_SET) in BGP_STATE_UP_LIST:
                state_brief = BGP_STATE_BRIEF_UP
            else:
                state_brief = BGP_STATE_BRIEF_DOWN

            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=neighbor,
                peer_hostname=facts.get('hostname', NOT_SET),
                remote_as=facts.get('asn', NOT_SET),
                state_brief=state_brief,
                session_state=facts.get('peerState', NOT_SET),
                state_time=facts.get('upDownTime', NOT_SET),
                prefix_received=facts.get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

        bgp_session_vrf = BGPSessionsVRF(
            vrf_name=vrf_name,
            as_number=cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('asn', NOT_SET),
            router_id=cmd_output.get('vrfs', NOT_SET).get(vrf_name, NOT_SET).get('routerId', NOT_SET),
            bgp_sessions=bgp_sessions_lst
        )

        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper BGP Converter
#
def _juniper_bgp_converter(hostname:str(), cmd_outputs:dict) -> BGP:

    if cmd_outputs is None:
        return None

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    for vrf_name in cmd_outputs.keys():

        # Create a BGP sessions list for each VRF
        bgp_sessions_lst = ListBGPSessions(
            list()
        )
        local_as = ""

        if 'bgp-peer' in cmd_outputs.get(vrf_name).get('bgp').get('bgp-information')[0].keys():
            for bgp_peer in cmd_outputs.get(vrf_name).get('bgp').get('bgp-information')[0].get('bgp-peer'):

                local_as = bgp_peer.get('local-as')[0].get('data', NOT_SET)

                if 'bgp-rib' in bgp_peer.keys():
                    prefix_received = bgp_peer.get('bgp-rib')[0].get('received-prefix-count')[0].get('data', NOT_SET)
                else:
                    prefix_received = NOT_SET

                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=_juniper_bgp_addr_filter(
                        bgp_peer.get('peer-address')[0].get('data', NOT_SET)
                    ),
                    peer_hostname=NOT_SET,
                    remote_as=bgp_peer.get('peer-as')[0].get('data', NOT_SET),
                    state_brief=_generic_state_converter(
                        bgp_peer.get('peer-state')[0].get('data', NOT_SET),
                    ),
                    session_state=bgp_peer.get('peer-state')[0].get('data', NOT_SET),
                    state_time=NOT_SET,
                    prefix_received=prefix_received,
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

            if vrf_name == "default":
                if 'conf' in cmd_outputs.get(vrf_name).keys():
                    if 'configuration' in cmd_outputs.get(vrf_name).get('conf').keys():
                        rid = cmd_outputs.get(vrf_name).get('conf').get('configuration').get('routing-options').get(
                            'router-id')
                    else:
                        rid = NOT_SET
                else:
                    rid = NOT_SET
            else:
                if 'conf' in cmd_outputs.get(vrf_name).keys():
                    if 'configuration' in cmd_outputs.get(vrf_name).get('conf').keys():
                        rid = cmd_outputs.get(vrf_name).get('conf').get('configuration').get('routing-instances').get(
                            'instance')[0].get('routing-options').get('router-id', NOT_SET)
                    else:
                        rid = NOT_SET
                else:
                    rid = NOT_SET

            bgp_session_vrf = BGPSessionsVRF(
                vrf_name=vrf_name,
                as_number=local_as,
                router_id=rid,
                bgp_sessions=bgp_sessions_lst
            )

            bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Juniper peer and local address filter
#
def _juniper_bgp_addr_filter(ip_addr:str) -> str:
    """
    This function will remove BGP (tcp) port of output information.
    Juniper output example :

    "peer-address" : [
            {
                "data" : "10.255.255.101+179"
            }
            ],
            "local-address" : [
            {
                "data" : "10.255.255.204+51954"
            }
            ],

    :param ip_addr:
    :return str: IP address without "+port"
    """

    if ip_addr.find("+") != -1:
        return ip_addr[:ip_addr.find("+")]
    else:
        return ip_addr