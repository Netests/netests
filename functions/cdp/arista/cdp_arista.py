#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotPossible


def _arista_get_cdp_api(task, options={}):
    raise NetestsFunctionNotPossible(
        "Arista - CDP - API - Not Available"
    )


def _arista_get_cdp_netconf(task):
    raise NetestsFunctionNotPossible(
        "Arista - CDP - NETCONF - Not Available"
    )


def _arista_get_cdp_ssh(task, options={}):
    raise NetestsFunctionNotPossible(
        "Arista - CDP - SSH - Not Available"
    )
