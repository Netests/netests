#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from protocols.lldp import LLDP, ListLLDP
from functions.global_tools import open_file
from functions.select_vars import select_host_vars
from const.constants import NOT_SET, LLDP_DATA_HOST_KEY, LLDP_WORKS_KEY
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported


HEADER = "[netests - compare_lldp]"


def compare_lldp(nr, options={}) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_lldp,
        options=options,
        on_failed=True,
        num_workers=10
    )

    return_value = True

    for value in data.values():
        if value.result is False:
            print(
                f"{HEADER} Task '_compare' has failed for "
                f"{value.host} (value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_lldp(task, options={}):

    task.host[LLDP_WORKS_KEY] = _compare_lldp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        lldp_host_data=task.host[LLDP_DATA_HOST_KEY],
        test=False,
        options=options,
        task=task

    )

    return task.host[LLDP_WORKS_KEY]


def _compare_lldp(
    host_keys,
    hostname,
    groups,
    lldp_host_data: ListLLDP,
    test=False,
    options={},
    task=Task
):

    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            lldp_yaml_data = open_file(
                path="tests/features/src/lldp_tests.yml"
            ).get(hostname)
        else:
            lldp_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="lldp"
            )

        verity_lldp = ListLLDP(
            list()
        )

        if LLDP_DATA_HOST_KEY in host_keys:
            for l in lldp_yaml_data:
                lldp_obj = LLDP(
                    local_name=hostname,
                    local_port=l.get("local_port", NOT_SET),
                    neighbor_name=l.get("neighbor_name", NOT_SET),
                    neighbor_port=l.get("neighbor_port", NOT_SET),
                    neighbor_os=l.get("neighbor_os", NOT_SET),
                    neighbor_mgmt_ip=l.get("neighbor_mgmt_ip", NOT_SET),
                    neighbor_type=l.get("neighbor_type", NOT_SET),
                )

                verity_lldp.lldp_neighbors_lst.append(lldp_obj)

            return verity_lldp == lldp_host_data

        else:
            print(f"Key {LLDP_DATA_HOST_KEY} is missing for {hostname}")
            return False
