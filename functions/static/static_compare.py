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
    from protocols.static import Static, ListStatic
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

########################################################################################################################
#
# Functions
#
def compare_static(nr, static_data:json) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    data = devices.run(
        task=_compare_static,
        static_data=static_data,
        on_failed=True,
        num_workers=10
    )
    #print_result(data)

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
def _compare_static(task, static_data:json, *, ansible_vars=False:bool, dict_keys="":str, your_keys={}:dict):
    pass

# ----------------------------------------------------------------------------------------------------------------------
#
# Compare function
#
def _retrieve_in_ansible_vars(task, dict_keys="":str, your_keys={}:dict) -> ListStatic:
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

        dyn_keys_lst = str(dict_keys).split(":")    
        res = task.host.get(dyn_keys_lst[0], {})
        
        if len(dyn_keys_lst) > 1:
            for key in dyn_keys_lst[1:]:
                res = res.get(key, {})
        
        for vrf_name, facts in res.items():
            
            prefix_key = your_keys.get('prefix', 'prefix')
            netmask_key = your_keys.get('netmask', 'netmask')
            nexthop_key = your_keys.get('nexthop', 'nexthop')
            preference_key = your_keys.get('preference', 'preference')
            metric_key = your_keys.get('metric', 'metric')   

            if acts.get('is_in_fib', NOT_SET) == NOT_SET:

                index_slash = str(facts.get(prefix_key).find("/")

                static_obj = Static(
                    vrf_name=vrf_name,
                    prefix=str(facts.get(prefix_key))[:index_slash],
                    netmask=str(facts.get(prefix_key))[index_slash+1:],
                    nexthop=facts.get(nexthop_key, NOT_SET),
                    is_in_fib=facts.get('is_in_fib', NOT_SET),
                    out_interface=facts.get('out_interface', NOT_SET),
                    preference=facts.get(preference_key, NOT_SET),
                    metric=facts.get(metric_key, NOT_SET)
                )
                
            else:

                static_obj = Static(
                    vrf_name=vrf_name,
                    prefix=facts.get(prefix_key, NOT_SET),
                    netmask=facts.get(netmask_key, NOT_SET),
                    nexthop=facts.get(nexthop_key, NOT_SET),
                    is_in_fib=facts.get('is_in_fib', NOT_SET),
                    out_interface=facts.get('out_interface', NOT_SET),
                    preference=facts.get(preference_key, NOT_SET),
                    metric=facts.get(metric_key, NOT_SET)
                )
    
            static_routes_lst.static_routes_lst.append(static_obj)    
                
    return static_routes_lst

"""
def find_in_dict(path_list, dic):
    if path_list and dic:
        res = dic.get(path_list[0], {})
        for key in path_list[1:]:
            res = res.get(key, {})
        return res
    return {}



a = ["a", "b", "c"]
dic_a = {"a": {"b": {"c": "yeah man"}}}
print(find_in_dict(a, dic_a))
"""

        




