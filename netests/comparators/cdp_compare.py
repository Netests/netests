#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.protocols.cdp import CDP, ListCDP
from netests.select_vars import select_host_vars
from netests.constants import NOT_SET, CDP_DATA_HOST_KEY, CDP_WORKS_KEY
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_cdp(task, options={}):
    task.host[CDP_WORKS_KEY] = _compare_cdp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        cdp_host_data=task.host.get(CDP_DATA_HOST_KEY, None),
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

        log.debug(
            "CDP_DATA_HOST_KEY in host_keys="
            f"{CDP_DATA_HOST_KEY in host_keys}\n"
            "cdp_yaml_data is not None="
            f"{cdp_yaml_data is not None}"
        )
        if (
            CDP_DATA_HOST_KEY in host_keys and
            cdp_yaml_data is not None
        ):
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

            log_compare(verity_cdp, cdp_host_data, hostname, groups)
            return verity_cdp == cdp_host_data

        else:
            log_no_yaml_data(
                "cdp",
                CDP_DATA_HOST_KEY,
                "CDP_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
