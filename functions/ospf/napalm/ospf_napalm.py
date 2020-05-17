#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _generic_ospf_napalm(task, options={}):
    raise NetestsFunctionNotPossible(
        "NAPALM - OSPF - Not possible"
    )
