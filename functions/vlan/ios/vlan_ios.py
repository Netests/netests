#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _ios_get_vlan_api(task):
    raise NetestsFunctionNotPossible(
        "Cisco IOS API functions is not supported..."
    )


def _ios_get_vlan_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco IOS Netconf functions is not implemented..."
    )


def _ios_get_vlan_ssh(task):
    raise NetestsFunctionNotImplemented(
        "Cisco IOS Netconf functions is not implemented..."
    )
