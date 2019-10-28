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
    from protocols.bgp import BGPSession, ListBGPSessions, BGP
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
# Cumulus BGP converter
#
def _cumulus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_lst = ListBGPSessions(list())
    as_number = ""
    router_id = ""

    for cmd_output in cmd_outputs:
        if "ipv4 unicast" in cmd_output.keys():
            if cmd_output.get('ipv4 unicast', NOT_SET) is NOT_SET:
                return list()

            else:

                if cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', NOT_SET) == "default":

                    if as_number == "" and router_id == "":
                        as_number = cmd_output.get('ipv4 unicast', NOT_SET).get('as', NOT_SET)
                        router_id = cmd_output.get('ipv4 unicast', NOT_SET).get('routerId', NOT_SET)

                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('peers', list()).items() :
                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                            vrf_name=cmd_output.get('ipv4 unicast', NOT_SET).get('vrfName', "default")
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

                else:
                    for peer_ip, facts in cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('peers', list()).items():
                        bgp_session = BGPSession(
                            src_hostname=hostname,
                            peer_ip=peer_ip,
                            peer_hostname=facts.get('hostname', NOT_SET),
                            remote_as=facts.get('remoteAs', NOT_SET),
                            session_state=facts.get('state', NOT_SET),
                            state_time=facts.get('peerUptime', NOT_SET),
                            prefix_received=facts.get('prefixReceivedCount', NOT_SET),
                            vrf_name=cmd_output.get('ipv4 unicast', NOT_SET).get('ipv4Unicast', NOT_SET).get('vrfName', "default")
                        )

                        bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=as_number,
        router_id=router_id,
        bgp_sessions=bgp_sessions_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus BGP Converter
#
def _nexus_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_lst = ListBGPSessions(list())

    for cmd_output in cmd_outputs:
        for neighbor in cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
                'ROW_neighbor', NOT_SET):
            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=neighbor.get('neighbor-id', NOT_SET),
                peer_hostname=neighbor.get('interfaces', NOT_SET),
                remote_as=neighbor.get('remoteas', NOT_SET),
                session_state=neighbor.get('state', NOT_SET),
                state_time=neighbor.get('LastUpDn', NOT_SET),
                prefix_received=neighbor.get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=cmd_output.get('localas', NOT_SET),
        router_id=cmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('router-id', NOT_SET),
        bgp_sessions=bgp_sessions_lst
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista BGP Converter
#
def _arista_bgp_converter(hostname:str(), cmd_outputs:list) -> BGP:

    bgp_sessions_lst = ListBGPSessions(list())

    for cmd_output in cmd_outputs:
        for neighbor, facts in cmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('peers', NOT_SET).items():
            bgp_session = BGPSession(
                src_hostname=hostname,
                peer_ip=neighbor,
                peer_hostname=facts.get('hostname', NOT_SET),
                remote_as=facts.get('asn', NOT_SET),
                session_state=facts.get('peerState', NOT_SET),
                state_time=facts.get('upDownTime', NOT_SET),
                prefix_received=facts.get('prefixReceived', NOT_SET)
            )

            bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=cmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('asn', NOT_SET),
        router_id=cmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('routerId', NOT_SET),
        bgp_sessions=bgp_sessions_lst
    )
