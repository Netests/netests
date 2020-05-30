#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.protocols.lldp import LLDP, ListLLDP
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.constants import NOT_SET, LLDP_DATA_HOST_KEY, LLDP_WORKS_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_lldp(task, options={}):

    task.host[LLDP_WORKS_KEY] = _compare_lldp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        lldp_host_data=task.host.get(LLDP_DATA_HOST_KEY, None),
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

        log.debug(
            "LLDP_DATA_HOST_KEY in host_keys="
            f"{LLDP_DATA_HOST_KEY in host_keys}\n"
            "lldp_yaml_data is not None="
            f"{lldp_yaml_data is not None}"
        )
        if (
            LLDP_DATA_HOST_KEY in host_keys and
            lldp_yaml_data is not None
        ):
            for nei in lldp_yaml_data:
                lldp_obj = LLDP(
                    local_name=hostname,
                    local_port=nei.get("local_port", NOT_SET),
                    neighbor_name=nei.get("neighbor_name", NOT_SET),
                    neighbor_port=nei.get("neighbor_port", NOT_SET),
                    neighbor_os=nei.get("neighbor_os", NOT_SET),
                    neighbor_mgmt_ip=nei.get("neighbor_mgmt_ip", NOT_SET),
                    neighbor_type=nei.get("neighbor_type", NOT_SET),
                )

                verity_lldp.lldp_neighbors_lst.append(lldp_obj)

            log_compare(verity_lldp, lldp_host_data, hostname, groups)
            return verity_lldp == lldp_host_data

        else:
            log_no_yaml_data(
                "lldp",
                LLDP_DATA_HOST_KEY,
                "LLDP_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
