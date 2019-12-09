#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate MTU protocols usage

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "1.0"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# Constantes
#
ERROR_HEADER = "Error import [bgp_tests.py]"
HEADER = "[netests - bgp_tests.py]"
########################################################################################################################
#
# Import Library
#

try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.static.static_converters import _arista_static_converter
    from functions.static.static_compare import _compare_static
    from protocols.static import ListNexthop, Nexthop, ListStatic, Static
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.static")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.global_tools import open_file
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from behave import given, when, then
except ImportError as importError:
    print(f"{ERROR_HEADER} behave")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import json
except ImportError as importError:
    print(f"{ERROR_HEADER} json")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import yaml
except ImportError as importError:
    print(f"{ERROR_HEADER} yaml")
    print(importError)
    exit(EXIT_FAILURE)

try:
    import textfsm
except ImportError as importError:
    print(f"{ERROR_HEADER} textfsm")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# Functions
#

@given(u'I create a Static python object manually named object_01')
def create_a_static_object_manually(context) -> None:
    """
    Create a Static object manually

    :param context:
    :return None:
    """

    static_routes_lst = ListStatic(
        static_routes_lst=list()
    )

    #
    ## 1st Object
    #
    nexthop_lst = ListNexthop(
        list()
    )

    nexthop_lst.nexthops_lst.append(
        Nexthop(
            ip_address='10.22.33.1',
            is_in_fib=True,
            out_interface='eth1/3',
            preference='1',
            metric='0',
            active=True
        )
    )

    static_routes_lst.static_routes_lst.append(
        Static(
            vrf_name='default',
            prefix='10.255.255.202',
            netmask='255.255.255.255',
            nexthop=nexthop_lst
        )
    )

    #
    ## 2nd Object
    #
    nexthop_lst = ListNexthop(
        list()
    )

    nexthop_lst.nexthops_lst.append(
        Nexthop(
            ip_address='10.1.3.1',
            is_in_fib=True,
            out_interface='eth1/1',
            preference='1',
            metric='0',
            active=True
        )
    )

    static_routes_lst.static_routes_lst.append(
        Static(
            vrf_name='default',
            prefix='10.255.255.101',
            netmask='255.255.255.255',
            nexthop=nexthop_lst
        )
    )

    #
    ## 3rd Object
    #
    nexthop_lst = ListNexthop(
        list()
    )

    nexthop_lst.nexthops_lst.append(Nexthop(
            ip_address='10.0.5.1',
            is_in_fib=True,
            out_interface='mgmt1',
            preference='1',
            metric='0',
            active=True
        )
    )

    static_routes_lst.static_routes_lst.append(
        Static(
            vrf_name='mgmt',
            prefix='0.0.0.0',
            netmask='0.0.0.0',
            nexthop=nexthop_lst
        )
    )

    context.object_01 = static_routes_lst


@given('I retrieve data from a YAML file to create a Static python object named object_02')
def create_a_static_object_from_a_json(context) -> None:
    """
    Retrieve data from a YAML file to compare with a Static object

    :param context:
    :return None:
    """

    yaml_content = open_file(
        path=f"{FEATURES_SRC_PATH}static_tests.yml"
    )

    context.object_02 = yaml_content


@given('I create a Static python object from a Arista output command named object_03')
def create_a_static_object_from_a_arista_output_command(context) -> None:
    """
    Create a Static object from a Arista output

    :param context:
    :return None:
    """

    cmd_outputs = list()

    cmd_outputs.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}arista_show_ip_route_static_default.json"
        )
    )

    cmd_outputs.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}arista_show_ip_route_static_mgmt.json"
        )
    )

    context.object_03 = _arista_static_converter(
        hostname="spine01",
        cmd_outputs=cmd_outputs
    )


@then('Static object_01 should be equal to object_02')
def compare_static_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_static(
        hostname="spine01",
        static_host_data=context.object_01,
        static_data=context.object_02,
        ansible_vars=False,
        dict_keys="",
        your_keys={},
        task=None
    )


@then('Static object_01 should be equal to object_03')
def compare_static_object_01_and_object_03(context) -> None:
    """
    Compare object_01 and object_03

    :param context:
    :return:
    """
    assert context.object_01 == context.object_03

@then('Static object_02 should be equal to object_03')
def compare_static_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """

    assert _compare_static(
        hostname="spine01",
        static_host_data=context.object_03,
        static_data=context.object_02,
        ansible_vars=False,
        dict_keys="",
        your_keys={},
        task=None
    )