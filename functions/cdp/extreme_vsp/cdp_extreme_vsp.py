#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _extreme_vsp_get_cdp_api(task, options={}):
    raise NetestsFunctionNotPossible(
        "Extreme VSP - CDP - API - Not Available"
    )

def _extreme_vsp_get_cdp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Extreme VSP - CDP - NETCONF - Not Available"
    )


def _extreme_vsp_get_cdp_ssh(task, options={}):
    raise NetestsFunctionNotPossible(
        "Extreme VSP - CDP - SSH - Not Available"
    )
