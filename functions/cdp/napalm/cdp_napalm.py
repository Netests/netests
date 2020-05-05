#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from exceptions.netests_exceptions import NetestsFunctionNotPossible

def _generic_cdp_napalm(task, options={}):
    raise NetestsFunctionNotPossible(
        "NAPALM doesn't get CDP informations..."
    )