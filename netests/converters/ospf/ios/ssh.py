#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.tools.cli import parse_textfsm
from netests.protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)


def _ios_ospf_ssh_converter(
    hostname: str,
    cmd_output,
    options={}
) -> OSPF:

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    print(cmd_output)

    if (
        (
            'data' in cmd_output.keys() or
            'rid' in cmd_output.keys()
        ) and
        (
            cmd_output.get('data') != '' or
            cmd_output.get('rid') != ''
        )

    ):
        cmd_output['data'] = parse_textfsm(
            content=cmd_output.get('data'),
            template_file='cisco_ios_show_ip_ospf_neighbor_detail.textfsm'
        )
        cmd_output['rid'] = parse_textfsm(
            content=cmd_output.get('rid'),
            template_file='cisco_ios_show_ip_ospf.textfsm'
        )
        cmd_output['int'] = parse_textfsm(
            content=cmd_output.get('int'),
            template_file='cisco_ios_show_ip_ospf_interface_brief.textfsm'
        )

        formated_data, mapping_router_id = _ios_format_data(
            cmd_outputs=cmd_output
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
                    for peer in formated_data.get(vrf) \
                                             .get(area) \
                                             .get(interface):
                        ospf_session_lst.ospf_sessions_lst.append(
                            OSPFSession(
                                peer_rid=peer.get('peer_rid'),
                                peer_hostname=NOT_SET,
                                session_state=peer.get(
                                    'session_state', NOT_SET
                                ),
                                local_interface=interface,
                                peer_ip=peer.get('peer_ip'),
                                options=options
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
                    router_id=mapping_router_id[vrf],
                    ospf_sessions_area_lst=ospf_area_lst
                )
            )

    return OSPF(
        hostname=hostname,
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )


def _ios_format_data(cmd_outputs: json) -> json:
    """
    This function will retrieve data from differents
    commands outputs and gegroup them in a structured data format.
    Three command are executed on devices
        -> show ip ospf neighbor detail
        -> show ip ospf interface
        -> show ip ospf

    :param cmd_outputs:
    :return json: Structured data
    """

    return_val = dict()
    result = dict()
    mapping_instance_vrf = dict()
    router_id = dict()

    if 'rid' in cmd_outputs.keys():
        for vrf in cmd_outputs.get('rid'):
            result[vrf[0]] = dict()

            if vrf[2] == '':
                return_val['default'] = dict()
                mapping_instance_vrf[vrf[0]] = 'default'
                router_id['default'] = vrf[1]
            else:
                return_val[vrf[2]] = dict()
                mapping_instance_vrf[vrf[0]] = vrf[2]
                router_id[vrf[2]] = vrf[1]

    if 'int' in cmd_outputs.keys():
        for i in cmd_outputs.get('int'):
            if i[1] in result.keys():
                if i[2] not in result.get(i[1]).keys():
                    result[i[1]][i[2]] = dict()
                result.get(i[1]) \
                      .get(i[2])[_mapping_interface_name(i[0])] = list()

    if 'data' in cmd_outputs.keys() and 'rid' in cmd_outputs.keys():
        for neighbor in cmd_outputs.get('data'):
            for instance_id in result:
                for area in result.get(instance_id):
                    if (
                        _mapping_interface_name(neighbor[3]) in
                        result.get(instance_id).get(area).keys()
                    ):

                        result.get(instance_id) \
                              .get(area) \
                              .get(_mapping_interface_name(neighbor[3])) \
                              .append(
                            {
                                'peer_rid': neighbor[0],
                                'peer_ip': neighbor[1],
                                'session_state': neighbor[4]
                            }
                        )

    for mapping in mapping_instance_vrf.keys():
        return_val[mapping_instance_vrf.get(mapping)] = result[mapping]

    return return_val, router_id


def _mapping_interface_name(int_name) -> str():
    """
    This function will receive an interface name in
    parameter and return the standard interface name.

    For example:
        * (Arista) Ethernet3 => Eth1/3

    :param int_name:
    :return:
    """

    if (
        "Ethernet1/" in int_name and
        "GIGABITETHERNET" not in str(int_name).upper()
    ):
        number = ""
        slash_index = int_name.find("/")
        for char in int_name[slash_index:]:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    elif (
        "Ethernet" in int_name and
        "GIGABITETHERNET" not in str(int_name).upper()
    ):
        number = ""
        for char in int_name:
            if str(char).isdigit():
                number = number + str(char)
        return str("Eth1/").lower() + str(number)

    elif "LOOPBACK" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("lo").lower() + int_name[index:]

    elif "MANAGEMENT" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("mgmt").lower() + int_name[index:]

    elif "GIGABITETHERNET" in str(int_name).upper():
        index = get_first_digit_index(int_name)
        return str("Gi") + str(int_name)[index:]

    elif "Gi" in str(int_name):
        index = get_first_digit_index(int_name)
        return str("Gi") + str(int_name)[index:]

    # Extreme VSP - Loopback converter
    # (Clip1        10.255.255.102 255.255.255.255)
    elif "Clip" in str(int_name):
        index = get_first_digit_index(int_name)
        return str("lo") + str(int_name)[index:]

    elif str(int_name) == NOT_SET:
        return int_name

    else:
        return str(int_name).lower()


def get_first_digit_index(string: str) -> int:
    """
    This function will return the index of the first index of a string.
    return -1 if no digit

    :param string: String on which one find a digit
    :return: Index of the first digit
    """
    index = 0
    find = False

    for char in str(string):
        if not find:
            if char.isdigit():
                find = True
            else:
                index = index + 1

    if not find:
        return -1
    return index
