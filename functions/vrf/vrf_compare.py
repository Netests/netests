#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os 
import json
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
from protocols.vrf import (
    VRF,
    ListVRF
)

    

ERROR_HEADER = "Error import [vrf_compare.py]"
HEADER_GET = "[netests - compare_vrf]"

def compare_vrf(nr) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_transit_vrf,
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
                f"{HEADER_GET} Task '_compare' has failed for {value.host}"
                f"(value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_vrf(task):
    task.host[VRF_WORKS_KEY] = _compare_vrf(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        vrf_host_data=task.host[VRF_DATA_KEY]
    )

    return task.host[VRF_WORKS_KEY]

def _compare_vrf(
    host_keys,
    hostname: str,
    groups: list,
    vrf_host_data: ListVRF,
    test=False
):
    verity_vrf = ListVRF(list())

    if test:
        vrf_yaml_data = open_file(
            path="tests/features/src/vrf_tests.yml"
        )
    else:
        vrf_yaml_data = select_host_vars(
            hostname=hostname,
            groups=groups,
            protocol="vrf"
        )

    if VRF_DATA_KEY in host_keys:
        for vrf in vrf_yaml_data.get(hostname, NOT_SET):

            vrf_obj = VRF(
                vrf_name=vrf.get('vrf_name', NOT_SET),
                vrf_id=vrf.get('vrf_id', NOT_SET),
                l3_vni=vrf.get('l3_vni', NOT_SET),
                rd=vrf.get('rd', NOT_SET),
                rt_imp=vrf.get('rt_imp', NOT_SET),
                rt_exp=vrf.get('rt_exp', NOT_SET),
                imp_targ=vrf.get('imp_targ', NOT_SET),
                exp_targ=vrf.get('exp_targ', NOT_SET),
            )

            verity_vrf.vrf_lst.append(vrf_obj)

        return verity_vrf == vrf_host_data

    else:
        print(f"Key {VRF_DATA_KEY} is missing for {hostname}")
        return False
