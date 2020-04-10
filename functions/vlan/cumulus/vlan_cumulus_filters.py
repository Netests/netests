#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json


def _filter_vlan_values(bond_lst: list, result_dict: dict, interface_name, vlan_id, filters: dict) -> dict:
    """
    This function will apply filters defined in netests configurations file.
    vlan:
      test: true
      filters:
        get_default: false
        get_bridge: false
        get_vni: false

    :param result_dict:
    :param interface_name:
    :param vlan_id:
    :return restult_dict:
    """

    if str(vlan_id) not in result_dict.keys():
        if str(vlan_id) == "1" and filters.get("get_default", True) is True or \
                str(vlan_id) != "1":
            result_dict[str(vlan_id)] = list()

    if str(vlan_id) in result_dict.keys():
        if ('bridge' in str(interface_name) and filters.get("get_bridge", True) is True) or \
                (str(interface_name) in bond_lst and filters.get("get_lag", True) is True) or \
                ('vni' in str(interface_name) and filters.get("get_vni", True) is True) or \
                ("bridge" not in str(interface_name) and "vni" not in str(interface_name) and
                 "peerlink" not in str(interface_name) and str(interface_name) not in bond_lst):

            if ('peerlink' in str(interface_name) and filters.get("get_peerlink", True) is True) or \
                    "peerlink" not in str(interface_name):

                result_dict.get(str(vlan_id)).append(str(interface_name))

    return result_dict


def _cumulus_vlan_members_converter(bond_lst: list, cmd_output: json, filters: dict) -> json:
    """
    On Cumulus devices with the command "net show bridge vlan json" you get the interface vlan members.
    Example :
        swp1 -> vlan100, vlan101, etc.
        swp2 -> vlan200, vlan101, etc
        vni100 -> vlan100

    This function will convert this output to have vlan interfaces members.
    Example :
        vlan100 -> swp1, vni100
        vlan101 -> swp1, swp2
        vlan200 -> swp2

    :param cmd_output:
    :return json:
    """

    if cmd_output is None:
        return None

    result_dict = dict()

    for interface_name in cmd_output:
        for vlan in cmd_output.get(interface_name):

            if "vlanEnd" in vlan.keys():
                i = 0
                while vlan.get("vlan") + i <= vlan.get("vlanEnd"):
                    result_dict = _filter_vlan_values(
                        bond_lst=bond_lst,
                        result_dict=result_dict,
                        interface_name=interface_name,
                        vlan_id=str(vlan.get("vlan")+i),
                        filters=filters
                    )
                    i += 1

            else:
                result_dict = _filter_vlan_values(
                    bond_lst=bond_lst,
                    result_dict=result_dict,
                    interface_name=interface_name,
                    vlan_id=str(vlan.get("vlan")),
                    filters=filters
                )

    return result_dict
