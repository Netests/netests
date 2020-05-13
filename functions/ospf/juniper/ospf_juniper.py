#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from jnpr.junos import Device
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.functions.text import print_result
from functions.http_request import exec_http_call_juniper
from nornir.plugins.tasks.networking import netmiko_send_command
from functions.ospf.juniper.api.converter import _juniper_ospf_api_converter
from functions.ospf.juniper.netconf.converter import _juniper_ospf_netconf_converter
from functions.ospf.juniper.ssh.converter import _juniper_ospf_ssh_converter
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    OSPF_SESSIONS_HOST_KEY,
    JUNOS_GET_OSPF_NEI,
    JUNOS_GET_OSPF_RID,
    JUNOS_GET_OSPF_NEI_VRF,
    JUNOS_GET_OSPF_RID_VRF,
    VRF_NAME_DATA_KEY,
    VRF_DEFAULT_RT_LST
)


def _juniper_get_ospf_api(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output_dict['default']['data'] = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="get-ospf-neighbor-information?instance=master&detail=",
        secure_api=task.host.get('secure_api', False)
    )
    output_dict['default']['rid'] = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="get-ospf-overview-information?instance=master",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(output_dict['default']['data'])
        print(output_dict['default']['rid'])

    for v in task.host[VRF_NAME_DATA_KEY].keys():
        if v not in VRF_DEFAULT_RT_LST:
            output_dict[v] = dict()
            output_dict[v]['data'] = exec_http_call_juniper(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                endpoint=f"get-ospf-neighbor-information?instance={v}&detail=",
                secure_api=task.host.get('secure_api', False)
            )
            output_dict[v]['rid'] = exec_http_call_juniper(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                endpoint=f"get-ospf-overview-information?instance={v}",
                secure_api=task.host.get('secure_api', False)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL5
            ):
                printline()
                print(output_dict[v]['data'])
                print(output_dict[v]['rid'])

    task.host[OSPF_SESSIONS_HOST_KEY] = _juniper_ospf_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _juniper_get_ospf_netconf(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:

        output_dict['default']['data'] = m.rpc.get_ospf_neighbor_information(
            detail=True,
            instance="master"
        )
        output_dict['default']['rid'] = m.rpc.get_ospf_overview_information(
            instance="master"
        )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL5
        ):
            printline()
            print(ElementTree.tostring(output_dict['default']['data']))
            print(ElementTree.tostring(output_dict['default']['rid']))

        ElementTree.fromstring(ElementTree.tostring(
            output_dict['default']['data'])
        )
        ElementTree.fromstring(ElementTree.tostring(
            output_dict['default']['rid'])
        )

        for vrf in task.host[VRF_NAME_DATA_KEY].keys():
            if vrf not in VRF_DEFAULT_RT_LST:
                output_dict[vrf] = dict()
                output_dict[vrf]['data'] = m.rpc.get_ospf_neighbor_information(
                    detail=True,
                    instance=vrf
                )
                output_dict[vrf]['rid'] = m.rpc.get_ospf_overview_information(
                    instance=vrf
                )
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL5
                ):
                    printline()
                    print(ElementTree.tostring(output_dict[vrf]['data']))
                    print(ElementTree.tostring(output_dict[vrf]['rid']))

                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf]['data'])
                )
                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf]['rid'])
                )

    task.host[OSPF_SESSIONS_HOST_KEY] = _juniper_ospf_netconf_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )


def _juniper_get_ospf_ssh(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output = task.run(
        name=f"{JUNOS_GET_OSPF_NEI}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_OSPF_NEI,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['data'] = output.result

    output = task.run(
        name=f"{JUNOS_GET_OSPF_RID}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_OSPF_RID,
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(output)

    output_dict['default']['rid'] = output.result

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output_dict[vrf] = dict()
            output = task.run(
                name=JUNOS_GET_OSPF_NEI_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_OSPF_NEI_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['data'] = output.result

            output = task.run(
                name=JUNOS_GET_OSPF_RID_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_OSPF_RID_VRF.format(vrf)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            output_dict[vrf]['rid'] = output.result

    task.host[OSPF_SESSIONS_HOST_KEY] = _juniper_ospf_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
