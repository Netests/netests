#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [static_compare.py]"
HEADER_GET = "[netests - compare_static]"

########################################################################################################################
#
# Default value used for exit()
#

try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from protocols.static import Nexthop, ListNexthop, Static, ListStatic
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.static")
    exit(EXIT_FAILURE)
    print(importError)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
    # To print task results
    from nornir.plugins.functions.text import print_result
except ImportError as importError:
    print(f"{ERROR_HEADER} nornir")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from main import open_file
except ImportError as importError:
    print(f"{ERROR_HEADER} main")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.global_tools import *
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#
def compare_static(nr, ansible_vars=False, dict_keys="", your_keys={} ) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    if ansible_vars is False:
        static_data = open_file(f"{PATH_TO_VERITY_FILES}{STATIC_SRC_FILENAME}")
    else:
        static_data = dict

    data = devices.run(
        task=_compare_static,
        static_data=static_data,
        ansible_vars=ansible_vars,
        dict_keys=dict_keys,
        your_keys=your_keys,
        on_failed=True,
        num_workers=10
    )
    print_result(data)

    return_value = True

    for value in data.values():
        if value.result is False:
            print(f"{HEADER_GET} Task '_compare' has failed for {value.host} (value.result={value.result}).")
            return_value = False

    return (not data.failed and return_value)

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _compare_static(task, static_data:json, *, ansible_vars=False, dict_keys="", your_keys={}):

    verity_static = ListStatic(
        static_routes_lst=list()
    )

    if ansible_vars:
        verity_static =  _retrieve_in_ansible_vars(
            task=task,
            dict_keys=dict_keys,
            your_keys=your_keys
        )

    else:

        for vrf_name, facts_lst in static_data.get(task.host.name).items():
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

    is_same = verity_static == task.host[STATIC_DATA_HOST_KEY]

    task.host[STATIC_WORKS_KEY] = is_same

    return is_same

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
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

