#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from protocols.cdp import CDP, ListCDP
from functions.global_tools import open_file
from functions.select_vars import select_host_vars
from const.constants import NOT_SET, CDP_DATA_HOST_KEY, CDP_WORKS_KEY
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported


HEADER = "[netests - compare_cdp]"


def compare_cdp(nr, options={}) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_cdp,
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


def _compare_transit_cdp(task, options={}):
    task.host[CDP_WORKS_KEY] = _compare_cdp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        cdp_host_data=task.host[CDP],
        test=False,
        options=options,
        task=task
    )

    return task.host[CDP_WORKS_KEY]


def _compare_cdp(
    host_keys,
    hostname,
    groups,
    cdp_host_data: ListCDP,
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
            cdp_yaml_data = open_file(
                path="tests/features/src/cdp_tests.yml"
            ).get(hostname)
        else:
            cdp_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="cdp"
            )

        verity_cdp = ListCDP(
            list()
        )

        if CDP_DATA_HOST_KEY in host_keys:
            for n in cdp_yaml_data:
                cdp_obj = CDP(
                    local_name=hostname,
                    local_port=n.get("local_port", NOT_SET),
                    neighbor_name=n.get("neighbor_name", NOT_SET),
                    neighbor_port=n.get("neighbor_port", NOT_SET),
                    neighbor_os=n.get("neighbor_os", NOT_SET),
                    neighbor_mgmt_ip=n.get("neighbor_mgmt_ip", NOT_SET),
                    neighbor_type=n.get("neighbor_type", NOT_SET),
                )

                verity_cdp.cdp_neighbors_lst.append(cdp_obj)

            return verity_cdp == cdp_host_data

        else:
            print(f"Key {CDP_DATA_HOST_KEY} is missing for {hostname}")
            return False
