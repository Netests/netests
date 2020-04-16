#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsFunctionNotImplemented


def _cumulus_get_facts_api(task, options={}):
    raise NetestsFunctionNotImplemented(
        "NXOS-FACT NOT IMPLEMENTED"
    )


def _cumulus_get_facts_netconf(task, options={}):
    raise NetestsFunctionNotImplemented(
        "CUMULUS-FACT NOT IMPLEMENTED"
    )


def _cumulus_get_facts_ssh(task, options={}):
    raise NetestsFunctionNotImplemented(
        "CUMULUS-FACT NOT IMPLEMENTED"
    )
