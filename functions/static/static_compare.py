#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from nornir.core.task import Task
from nornir.plugins.functions.text import print_result
from functions.verbose_mode import verbose_mode
from functions.global_tools import (
    open_file,
    is_cidr_notation,
    is_valid_cidr_netmask,
    convert_cidr_to_netmask
)
from functions.select_vars import select_host_vars
from const.constants import (
    NOT_SET,
    LEVEL2,
    STATIC_WORKS_KEY,
    STATIC_DATA_HOST_KEY,
    STATIC_SRC_FILENAME,
    PATH_TO_VERITY_FILES,
    TEST_TO_EXC_STATIC_KEY
)
from protocols.static import (
    Nexthop,
    ListNexthop,
    Static,
    ListStatic
)


HEADER = "[netests - static_compare]"


def compare_static(nr, own_vars={}) -> bool:
    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_static,
        own_vars=own_vars,
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


def _compare_transit_static(task, own_vars={}):
    task.host[STATIC_WORKS_KEY] =  _compare_static(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        static_host_data=task.host[STATIC_DATA_HOST_KEY],
        test=False,
        own_vars=own_vars,
        task=task
    )

    return task.host[STATIC_WORKS_KEY]


def _compare_static(
    host_keys,
    hostname: str,
    groups: list,
    static_host_data: ListStatic,
    test=False,
    own_vars={},
    task=Task
) -> bool:

    verity_static = ListStatic(static_routes_lst=list())

    if (
        own_vars is not None and
        'enable' in own_vars.keys() and
        own_vars.get('enable') is True
    ):
        verity_static = _retrieve_in_ansible_vars(
            task = task,
            dict_keys=own_vars.get('dict_keys', str()),
            your_keys=own_vars.get('your_keys', list())
        )
    else:
        if test:
            static_yaml_data = open_file(
                path="tests/features/src/static_tests.yml"
            )
        else:
            static_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="static" 
            )

        if STATIC_DATA_HOST_KEY in host_keys and hostname in static_yaml_data.keys():
            for vrf_name, facts_lst in static_yaml_data.get(hostname).items():
                for facts in facts_lst:

                    if facts.get('netmask', NOT_SET) == NOT_SET:

                        index_slash = str(facts.get('prefix')).find("/")

                        if is_cidr_notation(str(facts.get('prefix'))[index_slash + 1:]):
                            if is_valid_cidr_netmask(str(facts.get('prefix'))[index_slash + 1:]):
                                netmask = convert_cidr_to_netmask(str(facts.get('prefix'))[index_slash + 1:])
                            else:
                                netmask = NOT_SET
                        else:
                            netmask = str(facts.get('prefix'))[index_slash + 1:]

                        nexthops_lst = ListNexthop(
                            nexthops_lst=list()
                        )

                        for nexthop in facts.get('nexthop', NOT_SET):

                            nexthop_obj = Nexthop(
                                ip_address=nexthop.get('ip_address', NOT_SET),
                                is_in_fib=nexthop.get('is_in_fib', False),
                                out_interface=nexthop.get('out_interface', NOT_SET),
                                preference=nexthop.get('preference', NOT_SET),
                                metric=nexthop.get('metric', NOT_SET),
                                active=nexthop.get('metric', NOT_SET)
                            )

                            nexthops_lst.nexthops_lst.append(nexthop_obj)

                        static_obj = Static(
                            vrf_name=vrf_name,
                            prefix=str(facts.get('prefix'))[:index_slash],
                            netmask=netmask,
                            nexthop=nexthops_lst
                        )

                    else:

                        if is_cidr_notation(facts.get('netmask', NOT_SET)):
                            if is_valid_cidr_netmask(facts.get('netmask', NOT_SET)):
                                netmask = convert_cidr_to_netmask(facts.get('netmask', NOT_SET))
                            else:
                                netmask = NOT_SET
                        else:
                            netmask = facts.get('netmask', NOT_SET)

                        nexthops_lst = ListNexthop(
                            nexthops_lst=list()
                        )

                        for nexthop in facts.get('nexthop', NOT_SET):

                            nexthop_obj = Nexthop(
                                ip_address=nexthop.get('ip_address', NOT_SET),
                                is_in_fib=nexthop.get('is_in_fib', False),
                                out_interface=nexthop.get('out_interface', NOT_SET),
                                preference=nexthop.get('preference', NOT_SET),
                                metric=nexthop.get('metric', NOT_SET),
                                active=nexthop.get('metric', NOT_SET)
                            )

                            nexthops_lst.nexthops_lst.append(nexthop_obj)

                        static_obj = Static(
                            vrf_name=vrf_name,
                            prefix=facts.get('prefix', NOT_SET),
                            netmask=netmask,
                            nexthop=nexthops_lst
                        )

                    verity_static.static_routes_lst.append(static_obj)
        else:
            print(f"Key {STATIC_DATA_HOST_KEY} is missing for {hostname}")

    return verity_static == static_host_data


def _retrieve_in_ansible_vars(task, dict_keys="", your_keys={}) -> ListStatic:
    """
    This function will automatically retrieve data in Ansible vars.

    :param task: Nornir Task
    :param dict_keys: String contains keys to retreieve static route
    :param your_keys: Dictionnary containing keys using in vars_files
    :return ListStatic: List of static routes retrieve in Ansible vars files
    """

    static_routes_lst = ListStatic(
        static_routes_lst=list()
    )

    if dict_keys != "": 

        dyn_keys_lst = str(dict_keys).split(">")
        res = task.host.get(dyn_keys_lst[0], dict)

        if len(dyn_keys_lst) > 1:
            for key in dyn_keys_lst[1:]:
                res = res.get(key, {})

        for vrf_name, facts_lst in res.items():
            for facts in facts_lst:

                prefix_key = your_keys.get('prefix', 'prefix')
                netmask_key = your_keys.get('netmask', 'netmask')
                nexthop_key = your_keys.get('nexthop', 'nexthop')
                preference_key = your_keys.get('preference', 'preference')
                metric_key = your_keys.get('metric', 'metric')
                ip_address_key = your_keys.get('ip_address', 'ip')

                if facts.get(netmask_key, NOT_SET) == NOT_SET:

                    index_slash = str(facts.get(prefix_key)).find("/")

                    if is_cidr_notation(str(facts.get(prefix_key))[index_slash+1:]):
                        if is_valid_cidr_netmask(str(facts.get(prefix_key))[index_slash+1:]):
                            netmask = convert_cidr_to_netmask(str(facts.get(prefix_key))[index_slash+1:])
                        else:
                            netmask = NOT_SET
                    else:
                        netmask = str(facts.get(prefix_key))[index_slash+1:]

                    nexthops_lst = ListNexthop(
                        nexthops_lst=list()
                    )

                    for nexthop in facts.get(nexthop_key, NOT_SET):

                        nexthop_obj = Nexthop(
                            ip_address=nexthop.get(ip_address_key, NOT_SET),
                            is_in_fib=nexthop.get('is_in_fib', False),
                            out_interface=nexthop.get('out_interface', NOT_SET),
                            preference=nexthop.get(preference_key, NOT_SET),
                            metric=nexthop.get(metric_key, NOT_SET),
                            active=nexthop.get('active', NOT_SET)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                    static_obj = Static(
                        vrf_name=vrf_name,
                        prefix=str(facts.get(prefix_key))[:index_slash],
                        netmask=netmask,
                        nexthop=nexthops_lst
                    )
                
                else:

                    if is_cidr_notation(facts.get(netmask_key, NOT_SET)):
                        if is_valid_cidr_netmask(facts.get(netmask_key, NOT_SET)):
                            netmask = convert_cidr_to_netmask(facts.get(netmask_key, NOT_SET))
                        else:
                            netmask = NOT_SET
                    else:
                        netmask = facts.get(netmask_key, NOT_SET)

                    nexthops_lst = ListNexthop(
                        nexthops_lst=list()
                    )

                    for nexthop in facts.get(nexthop_key, NOT_SET):

                        nexthop_obj = Nexthop(
                            ip_address=nexthop.get(ip_address_key, NOT_SET),
                            is_in_fib=nexthop.get('is_in_fib', False),
                            out_interface=nexthop.get('out_interface', NOT_SET),
                            preference=nexthop.get(preference_key, NOT_SET),
                            metric=nexthop.get(metric_key, NOT_SET),
                            active=nexthop.get('active', NOT_SET)
                        )

                        nexthops_lst.nexthops_lst.append(nexthop_obj)

                    static_obj = Static(
                        vrf_name=vrf_name,
                        prefix=facts.get(prefix_key, NOT_SET),
                        netmask=netmask,
                        nexthop=nexthops_lst
                    )
    
                static_routes_lst.static_routes_lst.append(static_obj)

    return static_routes_lst

