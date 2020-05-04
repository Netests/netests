#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _juniper_get_vlan_api(task):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks API functions is not implemented..."
    )


def _juniper_get_vlan_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks Netconf functions is not implemented..."
    )


def _juniper_get_vlan_ssh(task):
    raise NetestsFunctionNotImplemented(
        "Juniper Networks SSH functions is not implemented..."
    )
