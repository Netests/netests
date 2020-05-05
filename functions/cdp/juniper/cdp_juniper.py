#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _juniper_get_cdp_api(task, options={}):
    raise NetestsFunctionNotPossible(
        "Juniper - CDP - API - Not Available"
    )

def _juniper_get_cdp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Juniper - CDP - NETCONF - Not Available"
    )


def _juniper_get_cdp_ssh(task, options={}):
    raise NetestsFunctionNotPossible(
        "Juniper - CDP - SSH - Not Available"
    )
