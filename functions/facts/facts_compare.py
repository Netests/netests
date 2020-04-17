#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from const.constants import FACTS_WORKS_KEY, FACTS_DATA_HOST_KEY
from protocols.facts import Facts
# from nornir.plugins.functions.text import print_result


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
    # print_result(data)

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
    """
    verity_infos = SystemInfos()

    if FACTS_DATA_HOST_KEY in host_keys:
        if hostname in infos_data.keys():

            facts = Facts(
                hostname = hostname
                domain = infos_data.get(hostname)
                                   .get('domain', NOT_SET)
                version = infos_data.get(hostname)
                                    .get('version', NOT_SET)
                serial = infos_data.get(hostname)
                                   .get('serial', NOT_SET)
                base_mac = infos_data.get(hostname)
                                     .get('serial', NOT_SET)
                memory = infos_data.get(hostname)
                                   .get('memory', NOT_SET)
                vendor = infos_data.get(hostname)
                                   .get('vendor', NOT_SET)
                model = infos_data.get(hostname)
                                  .get('model', NOT_SET)
                snmp_ips = infos_data.get(hostname)
                                     .get('snmp_ips', list())
                interfaces_lst = infos_data.get(hostname)
                                           .get('interfaces', list())
            )

        return verity_infos == infos_host_data

    else:
        print(f"Key {FACTS_DATA_HOST_KEY} is missing for {hostname}")
        return False
    """
