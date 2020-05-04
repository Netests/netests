#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import (
    NetestsFunctionNotPossible,
    NetestsFunctionNotImplemented
)


def _extreme_vsp_get_vlan_api(task, options={}):
    raise NetestsFunctionNotPossible(
        "Extreme Networks API functions is not supported..."
    )


def _extreme_vsp_get_vlan_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "Extreme Networks Netconf functions is not implemented..."
    )


def _extreme_vsp_get_vlan_ssh(task, options={}):
    raise NetestsFunctionNotImplemented(
        "Extreme Networks Netconf functions is not implemented..."
    )
