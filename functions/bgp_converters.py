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
    print(f"{ERROR_HEADER} nornir")
    exit(EXIT_FAILURE)
    print(importError)

########################################################################################################################
#
# Import Library
#
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
def _cumulus_bgp_converter(hostname:str(), cmd_output:dict()) -> BGP:

    bgp_sessions_lst = ListBGPSessions(list())

    jcmd_output = json.loads(cmd_output)

    if "ipv4 unicast" in jcmd_output.keys():
        if jcmd_output.get('ipv4 unicast', NOT_SET) is NOT_SET:
            return list()

        else:
            for peer_ip, facts in jcmd_output.get('ipv4 unicast', NOT_SET).get('peers', list()).items() :
                bgp_session = BGPSession(
                    src_hostname=hostname,
                    peer_ip=peer_ip,
                    peer_hostname=facts.get('hostname', NOT_SET),
                    remote_as=facts.get('remoteAs', NOT_SET),
                )

                bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=jcmd_output.get('ipv4 unicast', NOT_SET).get('as', NOT_SET),
        router_id=jcmd_output.get('ipv4 unicast', NOT_SET).get('routerId', NOT_SET),
        bgp_sessions=bgp_sessions_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
# Cisco Nexus BGP Converter
#
def _nexus_bgp_converter(hostname:str(), cmd_output:dict()) -> BGP:

    bgp_sessions_lst = ListBGPSessions(list())

    jcmd_output = json.loads(cmd_output)

    for neighbor in jcmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('TABLE_neighbor', NOT_SET).get(
            'ROW_neighbor', NOT_SET):
        bgp_session = BGPSession(
            src_hostname=hostname,
            peer_ip=neighbor.get('neighbor-id', NOT_SET),
            peer_hostname=neighbor.get('interfaces', NOT_SET),
            remote_as=neighbor.get('remoteas', NOT_SET)
        )

        bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=jcmd_output.get('localas', NOT_SET),
        router_id=jcmd_output.get('TABLE_vrf', NOT_SET).get('ROW_vrf', NOT_SET).get('router-id', NOT_SET),
        bgp_sessions=bgp_sessions_lst
    )


# ----------------------------------------------------------------------------------------------------------------------
#
# Arista BGP Converter
#
def _arista_bgp_converter(hostname:str(), cmd_output:dict()) -> ListBGPSessions:

    bgp_sessions_lst = ListBGPSessions(list())

    jcmd_output = json.loads(cmd_output)

    for neighbor, facts in jcmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('peers', NOT_SET).items():
        bgp_session = BGPSession(
            src_hostname=hostname,
            peer_ip=neighbor,
            peer_hostname=facts.get('hostname', NOT_SET),
            remote_as=facts.get('asn', NOT_SET)
        )

        bgp_sessions_lst.bgp_sessions.append(bgp_session)

    return BGP(
        hostname=hostname,
        as_number=jcmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('asn', NOT_SET),
        router_id=jcmd_output.get('vrfs', NOT_SET).get('default', NOT_SET).get('routerId', NOT_SET),
        bgp_sessions=bgp_sessions_lst
    )
