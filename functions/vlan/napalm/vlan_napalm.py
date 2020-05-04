#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _generic_vlan_napalm(task):
    raise NetestsFunctionNotImplemented(
        "NAPALM VLAN functions is not implemented..."
    )
