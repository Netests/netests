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
from const.constants import (
    NOT_SET,
    LEVEL2,
    LEVEL5,
    BGP_SESSIONS_HOST_KEY,
    JUNOS_GET_BGP,
    JUNOS_GET_BGP_RID,
    JUNOS_GET_BGP_VRF,
    JUNOS_GET_BGP_VRF_RID,
    VRF_DATA_KEY,
    VRF_DEFAULT_RT_LST
)
from functions.bgp.juniper.api.converter import (
    _juniper_bgp_api_converter
)
from functions.bgp.juniper.netconf.converter import (
    _juniper_bgp_netconf_converter
)
from functions.bgp.juniper.ssh.converter import (
    _juniper_bgp_ssh_converter
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_get_bgp_api(task, options={}):
    output_dict = dict()
    output_dict['default'] = dict()
    output_dict['default']['bgp'] = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="get-bgp-neighbor-information?exact-instance=master",
        secure_api=task.host.get('secure_api', False)
    )
    output_dict['default']['rid'] = exec_http_call_juniper(
        hostname=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        endpoint="get-instance-information?instance-name=master&detail=",
        secure_api=task.host.get('secure_api', False)
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(output_dict['default']['rid'])
        print(output_dict['default']['rid'])

    for v in task.host[VRF_DATA_KEY].vrf_lst:
        if v.vrf_name not in VRF_DEFAULT_RT_LST:
            output_dict[v.vrf_name] = dict()
            output_dict[v.vrf_name]['bgp'] = exec_http_call_juniper(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                endpoint=f"get-bgp-neighbor-information?exact-instance={v.vrf_name}",
                secure_api=task.host.get('secure_api', False)
            )
            output_dict[v.vrf_name]['rid'] = exec_http_call_juniper(
                hostname=task.host.hostname,
                port=task.host.port,
                username=task.host.username,
                password=task.host.password,
                endpoint=f"get-instance-information?instance-name={v.vrf_name}&detail=",
                secure_api=task.host.get('secure_api', False)
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL5
            ):
                printline()
                print(output_dict[v.vrf_name]['bgp'])
                print(output_dict[v.vrf_name]['rid'])

    task.host[BGP_SESSIONS_HOST_KEY] = _juniper_bgp_api_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
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

        for vrf in task.host[VRF_DATA_KEY].vrf_lst:
            if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
                output_dict[vrf.vrf_name] = dict()
                output_dict[vrf.vrf_name]['bgp'] = m.rpc.get_bgp_neighbor_information(
                    exact_instance=vrf.vrf_name
                )
                output_dict[vrf.vrf_name]['rid'] = m.rpc.get_instance_information(
                    detail=True,
                    instance_name=vrf.vrf_name
                )
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL5
                ):
                    printline()
                    print(ElementTree.tostring(
                        output_dict[vrf.vrf_name]['bgp'])
                    )
                    print(ElementTree.tostring(
                        output_dict[vrf.vrf_name]['rid'])
                    )

                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf.vrf_name]['bgp'])
                )
                ElementTree.fromstring(
                    ElementTree.tostring(output_dict[vrf.vrf_name]['rid'])
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
        output_dict["default"]["rid"] = output.result

    for vrf in task.host[VRF_DATA_KEY].vrf_lst:
        if vrf.vrf_name not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=JUNOS_GET_BGP_VRF.format(vrf.vrf_name),
                task=netmiko_send_command,
                command_string=JUNOS_GET_BGP_VRF.format(vrf.vrf_name),
            )
            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL2
            ):
                print_result(output)

            if (
                output.result != "" and
                "BGP is not running" not in output.result
            ):
                output_dict[vrf.vrf_name] = dict()
                output_dict[vrf.vrf_name]["bgp"] = output.result

                output = task.run(
                    name=JUNOS_GET_BGP_VRF_RID.format(vrf.vrf_name),
                    task=netmiko_send_command,
                    command_string=JUNOS_GET_BGP_VRF_RID.format(vrf.vrf_name),
                )
                if verbose_mode(
                    user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                    needed_value=LEVEL2
                ):
                    print_result(output)

                if (
                    output.result != "" and
                    "BGP is not running" not in output.result
                ):
                    output_dict[vrf.vrf_name]["rid"] = output.result

    task.host[BGP_SESSIONS_HOST_KEY] = _juniper_bgp_ssh_converter(
        hostname=task.host.name,
        cmd_output=output_dict,
        options=options
    )
