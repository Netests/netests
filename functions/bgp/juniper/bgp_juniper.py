#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import xmltodict
from jnpr.junos import Device
from xml.etree import ElementTree
from functions.verbose_mode import verbose_mode
from functions.http_request import exec_http_nxos
from nornir.plugins.functions.text import print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    BGP_SESSIONS_HOST_KEY,
    JUNOS_GET_BGP,
    JUNOS_GET_BGP_RID,
    JUNOS_GET_BGP_VRF,
    JUNOS_GET_BGP_VRF_RID,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.juniper.ssh.converter import (
    _juniper_bgp_ssh_converter
)
from functions.bgp.juniper.netconf.converter import (
    _juniper_bgp_netconf_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_get_bgp_api(task):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks API functions is not implemented..."
    )


def _juniper_get_bgp_netconf(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:

        output_dict['default']['bgp'] = m.rpc.get_bgp_neighbor_information(
            exact_instance="master"
        )
        output_dict['default']['rid'] = m.rpc.get_instance_information(
            detail=True,
            instance_name="master"
        )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL5
        ):
            printline()
            print(ElementTree.tostring(output_dict['default']['bgp']))
            print(ElementTree.tostring(output_dict['default']['rid']))
        
        ElementTree.fromstring(ElementTree.tostring(
            output_dict['default']['bgp'])
        )
        ElementTree.fromstring(ElementTree.tostring(
            output_dict['default']['rid'])
        )

        for vrf in task.host[VRF_NAME_DATA_KEY].keys():
            if vrf not in VRF_DEFAULT_RT_LST:
                output_dict[vrf] = dict()
                output_dict[vrf]['bgp'] = m.rpc.get_bgp_neighbor_information(
                    exact_instance=vrf
                )
                output_dict[vrf]['rid'] = m.rpc.get_instance_information(
                    detail=True,
                    instance_name=vrf
                )
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL5
                ):
                    printline()
                    print(ElementTree.tostring(output_dict[vrf]['bgp']))
                    print(ElementTree.tostring(output_dict[vrf]['rid']))

                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf]['bgp'])
                )
                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf]['rid'])
                )

    task.host[BGP_SESSIONS_HOST_KEY] = _juniper_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _juniper_get_bgp_ssh(task, options={}):
    output_dict = dict()
    output_dict["default"] = dict()
    output = task.run(
        name=f"{JUNOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_BGP
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "" and "BGP is not running" not in output.result:
        output_dict["default"]["bgp"] = output.result
    
    output = task.run(
        name=f"{JUNOS_GET_BGP_RID}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_BGP_RID,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    if output.result != "" and "BGP is not running" not in output.result:
        output_dict["default"]["conf"] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=JUNOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_BGP_VRF.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if (
                output.result != "" and
                "router-id" in output.result and
                "BGP is not running" not in output.result
            ):
                output_dict[vrf] = dict()
                output_dict[vrf]["bgp"] = output.result

            output = task.run(
                name=JUNOS_GET_BGP_VRF_RID.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_BGP_VRF_RID.format(vrf),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if (
                output.result != "" and
                "router-id" in output.result and
                "BGP is not running" not in output.result
            ):
                output_dict[vrf]["conf"] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _juniper_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
