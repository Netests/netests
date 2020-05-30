#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.protocols.facts import Facts
from netests.select_vars import select_host_vars
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.constants import NOT_SET, FACTS_WORKS_KEY, FACTS_DATA_HOST_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_facts(task, options={}):

    task.host[FACTS_WORKS_KEY] = _compare_facts(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        facts_host_data=task.host.get(FACTS_DATA_HOST_KEY, None),
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

        log.debug(
            "FACTS_DATA_HOST_KEY in host_keys="
            f"{FACTS_DATA_HOST_KEY in host_keys}\n"
            "facts_yaml_data is not None="
            f"{facts_yaml_data is not None}"
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

            log_compare(verity_facts, facts_host_data, hostname, groups)
            return verity_facts == facts_host_data

        else:
            log_no_yaml_data(
                "facts",
                FACTS_DATA_HOST_KEY,
                "FACTS_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
