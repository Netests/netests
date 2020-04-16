#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _arista_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "ARISTA-FACT NOT IMPLEMENTED"
    )


def _arista_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "ARISTA-FACT NOT IMPLEMENTED"
    )


def _arista_get_facts_ssh(task, options={}):
    raise NetestsFunctionNotImplemented(
        "ARISTA-FACT NOT IMPLEMENTED"
    )
