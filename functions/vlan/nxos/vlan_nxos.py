#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _nxos_get_vlan_api(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus NXOS API functions is not implemented...."
    )


def _nxos_get_vlan_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus NXOS Netconf functions is not implemented..."
    )


def _nxos_get_vlan_ssh(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus NXOS SSH functions is not implemented...."
    )
