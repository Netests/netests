#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.protocols.vrf import VRF, ListVRF
from netests.select_vars import select_host_vars
from netests.constants import NOT_SET, VRF_DATA_KEY, VRF_WORKS_KEY
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_vrf(task, options={}):
    task.host[VRF_WORKS_KEY] = _compare_vrf(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vrf_host_data=task.host.get(VRF_DATA_KEY, None),
        test=False,
        options=options,
        task=task
    )

    return task.host[VRF_WORKS_KEY]


def _compare_vrf(
    host_keys,
    hostname: str,
    groups: list,
    vrf_host_data: ListVRF,
    test=False,
    options={},
    task=Task
) -> bool:
    verity_vrf = ListVRF(list())

    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            vrf_yaml_data = open_file(
                path="tests/features/src/vrf_tests.yml"
            ).get(hostname)
        else:
            vrf_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="vrf"
            )

        log.debug(
            "VRF_DATA_KEY in host_keys="
            f"{VRF_DATA_KEY in host_keys}\n"
            "vrf_yaml_data is not None="
            f"{vrf_yaml_data is not None}"
        )
        if (
            VRF_DATA_KEY in host_keys and
            vrf_yaml_data is not None
        ):
            if vrf_yaml_data is not None:
                for vrf in vrf_yaml_data:
                    verity_vrf.vrf_lst.append(
                        VRF(
                            vrf_name=vrf.get('vrf_name', NOT_SET),
                            vrf_id=vrf.get('vrf_id', NOT_SET),
                            l3_vni=vrf.get('l3_vni', NOT_SET),
                            rd=vrf.get('rd', NOT_SET),
                            rt_imp=vrf.get('rt_imp', NOT_SET),
                            rt_exp=vrf.get('rt_exp', NOT_SET),
                            imp_targ=vrf.get('imp_targ', NOT_SET),
                            exp_targ=vrf.get('exp_targ', NOT_SET)
                        )
                    )

            log_compare(verity_vrf, vrf_host_data, hostname, groups)
            return verity_vrf == vrf_host_data

        else:
            log_no_yaml_data(
                "vrf",
                VRF_DATA_KEY,
                "VRF_DATA_KEY",
                hostname,
                groups
            )
            return True
