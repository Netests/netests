#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core.task import Task
from protocols.facts import Facts
from functions.verbose_mode import verbose_mode
from functions.select_vars import select_host_vars
from functions.global_tools import open_file
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported
from const.constants import (
    NOT_SET,
    LEVEL2,
    FACTS_WORKS_KEY,
    FACTS_DATA_HOST_KEY
)


HEADER = "[netests - compare_infos]"


def compare_facts(nr, options={}) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_facts,
        options=options,
        on_failed=True,
        num_workers=10
    )

    return_value = True
    for value in data.values():
        if value.result is False:
            print(
                f"\t{HEADER} Task '_compare' has failed for {value.host} "
                f"(value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_facts(task, options={}):

    task.host[FACTS_WORKS_KEY] = _compare_facts(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        facts_host_data=task.host[FACTS_DATA_HOST_KEY],
        test=False,
        options=options,
        task=task
    )

    return task.host[FACTS_WORKS_KEY]


def _compare_facts(
    host_keys,
    hostname: str,
    groups: list,
    facts_host_data: Facts,
    test=False,
    options={},
    task=Task
) -> bool:
    pass
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            facts_yaml_data = open_file(
                path="tests/features/src/facts_tests.yml"
            ).get(hostname)
        else:
            facts_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="facts"
            )

        if (
            FACTS_DATA_HOST_KEY in host_keys and
            facts_yaml_data is not None
        ):
            verity_facts = Facts(
                hostname=hostname,
                domain=facts_yaml_data.get('domain', NOT_SET),
                version=facts_yaml_data.get('version', NOT_SET),
                build=facts_yaml_data.get('build', NOT_SET),
                serial=facts_yaml_data.get('serial', NOT_SET),
                base_mac=facts_yaml_data.get('serial', NOT_SET),
                memory=facts_yaml_data.get('memory', NOT_SET),
                vendor=facts_yaml_data.get('vendor', NOT_SET),
                model=facts_yaml_data.get('model', NOT_SET),
                interfaces_lst=facts_yaml_data.get('interfaces', list()),
                options=facts_host_data.options
            )

        else:
            print(
                f"{HEADER} Key {FACTS_DATA_HOST_KEY} is missing"
                f"for {hostname} or no Facts data has been found."
            )
            return False

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print(
            f"{HEADER} Return value for host {hostname}"
            f"is {verity_facts == facts_host_data}"
        )

    return verity_facts == facts_host_data
