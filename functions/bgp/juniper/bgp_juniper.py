#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import xmltodict
from ncclient import manager
from xml.etree import ElementTree
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    NETCONF_FILTER,
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


def _juniper_get_bgp_api(task):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks API functions is not implemented..."
    )


def _juniper_get_bgp_netconf(task):
    with manager.connect(
        host=task.host.hostname,
        port=task.host.port,
        username=task.host.username,
        password=task.host.password,
        hostkey_verify=False
    ) as m:

        bgp_config = m.get_config(
            source='running',
            filter=NETCONF_FILTER.format(
                (
                    "<configuration>"
                    "<protocols>"
                    "<bgp/>"
                    "</protocols>"
                    "</configuration>"
                )
            )
        ).data_xml

    ElementTree.fromstring(bgp_config)

    task.host[BGP_SESSIONS_HOST_KEY] = _juniper_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_outputs=json.dumps(xmltodict.parse(bgp_config))
    )


def _juniper_get_bgp_ssh(task):
    outputs_lst = dict()
    outputs_lst["default"] = dict()
    output = task.run(
        name=f"{JUNOS_GET_BGP}",
        task=netmiko_send_command,
        command_string=JUNOS_GET_BGP
    )

    if output.result != "":
        outputs_lst["default"]["bgp"] = json.loads(output.result)
        output = task.run(
            name=f"{JUNOS_GET_BGP_RID}",
            task=netmiko_send_command,
            command_string=JUNOS_GET_BGP_RID,
        )

        if output.result != "":
            outputs_lst["default"]["conf"] = json.loads(output.result)

    for vrf in task.host[VRF_NAME_DATA_KEY].keys():
        if vrf not in VRF_DEFAULT_RT_LST:
            output = task.run(
                name=JUNOS_GET_BGP_VRF.format(vrf),
                task=netmiko_send_command,
                command_string=JUNOS_GET_BGP_VRF.format(vrf),
            )

            if output.result != "" and "bgp-peer" in output.result:
                outputs_lst[vrf] = dict()
                outputs_lst[vrf]["bgp"] = json.loads(output.result)

                output = task.run(
                    name=JUNOS_GET_BGP_VRF_RID.format(vrf),
                    task=netmiko_send_command,
                    command_string=JUNOS_GET_BGP_VRF_RID.format(vrf),
                )

                if output.result != "" and "router-id" in output.result:
                    outputs_lst[vrf]["conf"] = json.loads(output.result)

    bgp_sessions = _juniper_bgp_ssh_converter(task.host.name, outputs_lst)
    task.host[BGP_SESSIONS_HOST_KEY] = bgp_sessions
