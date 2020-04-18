#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core.task import Task
from functions.verbose_mode import verbose_mode
from functions.select_vars import select_host_vars
from functions.global_tools import open_file
from nornir.plugins.functions.text import print_result
from const.constants import (
    NOT_SET,
    LEVEL2,
    VRF_DATA_KEY,
    VRF_WORKS_KEY
)
from protocols.vrf import VRF, ListVRF
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported


HEADER = "[netests - compare_vrf]"


def compare_vrf(nr, options={}) -> bool:
    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_vrf,
        options=options,
        on_failed=True,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(
                f"{HEADER} Task '_compare' has failed for {value.host}"
                f"(value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_vrf(task, options={}):
    task.host[VRF_WORKS_KEY] = _compare_vrf(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vrf_host_data=task.host[VRF_DATA_KEY],
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

        print(
            f"{HEADER} Key {VRF_DATA_KEY} is missing"
            f"for {hostname} or no VRF data has been found."
        )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(
            f"{HEADER} Return value for host {hostname}"
            f"is {verity_vrf == vrf_host_data}"
        )
    return verity_vrf == vrf_host_data
