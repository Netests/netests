#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.protocols.vlan import VLAN
from netests.select_vars import select_host_vars
from netests.comparators.log_compare import log_no_yaml_data
from netests.constants import VLAN_WORKS_KEY, VLAN_DATA_HOST_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_vlan(task, options={}):

    task.host[VLAN_WORKS_KEY] = _compare_vlan(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vlan_host_data=task.host.get(VLAN_DATA_HOST_KEY, None),
        test=False,
        options=options,
        task=task
    )

    return task.host[VLAN_WORKS_KEY]


def _compare_vlan(
    host_keys,
    hostname: str,
    groups: list,
    vlan_host_data: VLAN,
    test=False,
    options={},
    task=Task
) -> bool:
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            vlan_yaml_data = open_file(
                path="tests/features/src/vlan_tests.yml"
            ).get(hostname)
        else:
            vlan_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="vlan"
            )

        log.debug(
            "VLAN_DATA_HOST_KEY in host_keys="
            f"{VLAN_DATA_HOST_KEY in host_keys}\n"
            "vlan_yaml_data is not None="
            f"{vlan_yaml_data is not None}"
        )
        if (
            VLAN_DATA_HOST_KEY in host_keys and
            vlan_yaml_data is not None
        ):
            print(f"IMPLEMENT {__file__}")

        else:
            log_no_yaml_data(
                "vlan",
                VLAN_DATA_HOST_KEY,
                "VLAN_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
