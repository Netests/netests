#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import xmltodict
from ncclient import manager
from xml.etree import ElementTree
from const.constants import (
    NETCONF_FILTER,
    BGP_SESSIONS_HOST_KEY
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented,
    NetestsFunctionNotPossible
)
# from functions.bgp.iosxr.api.converter import _iosxr_bgp_api_converter
from functions.bgp.iosxr.netconf.converter import _iosxr_bgp_netconf_converter
# from functions.bgp.iosxr.ssh.converter import _iosxr_bgp_ssh_converter


def _iosxr_get_bgp_api(task):
    raise NetestsFunctionNotPossible(
        "Cisco IOS-XR does not support HTTP REST API..."
    )


def _iosxr_get_bgp_netconf(task, options={}):
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
                "<bgp "
                "xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ipv4-bgp-cfg\""
                "/>"
            )
        ).data_xml

    ElementTree.fromstring(bgp_config)

    task.host[BGP_SESSIONS_HOST_KEY] = _iosxr_bgp_netconf_converter(
        hostname=task.host.name,
        cmd_output=bgp_config,
        options=options
    )


def _iosxr_get_bgp_ssh(task):
    raise NetestsFunctionNotImplemented(
        "Cisco IOS-XR SSH functions is not implemented..."
    )
