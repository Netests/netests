#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate IPV6 protocols usage

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
ERROR_HEADER = "Error import [ipv6_tests.py]"
HEADER = "[netests - ipv6_tests.py]"
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
    from functions.ip.ipv6.ipv6_converters import _cumulus_ipv6_converter, _nexus_ipv6_converter, _arista_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _ios_ipv6_converter, _juniper_ipv6_converter
    from functions.ip.ipv6.ipv6_converters import _napalm_ipv6_converter, _extreme_vsp_ipv6_converter
    from functions.ip.ipv6.ipv6_compare import _compare_ipv6
    from protocols.ipv6 import IPV6Interface, ListIPV6Interface
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ip.ipv6 ")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.global_tools import open_file, open_txt_file
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

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given(u'I create an IPV6 python object corresponding to Arista device manually named object_01')
def create_an_ipv6_object_manually(context) -> None:
    """
    Create a IPV6 object manually

    :param context:
    :return None:
    """

    ipv6_addresses_lst = ListIPV6Interface(
        ipv6_addresses_lst=list()
    )

    ipv6_addresses_lst.ipv6_addresses_lst.append(
        IPV6Interface(
            interface_name="eth1/2",
            ip_address_with_mask="2001:cafe:c0ca:203::2/64",
        )
    )

    ipv6_addresses_lst.ipv6_addresses_lst.append(
        IPV6Interface(
            interface_name="eth1/1",
            ip_address_with_mask="2001:cafe:c0ca:103::2/64",
        )
    )

    context.object_01 = ipv6_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an IPV6 python object named object_02')
def create_an_ipv6_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
        Retrieve data from a YAML file to compare with a IPV6 object

        :param context:
        :return None:
        """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}ipv6_tests.yml"
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an IPV6 python object from a Arista output command named object_03')
def create_an_ipv6_object_from_a_arista_output_command(context) -> None:
    """
    Create an IPV6 object from a Arista output

    :param context:
    :return None:
    """

    context.object_03 = _arista_ipv6_converter(
        hostname="leaf03",
        plateform="eos",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}arista_show_ipv6_interface.json"
        ),
        filters={
            "get_loopback": True,
            "get_physical": True,
            "get_vlan": True,
            "get_peerlink": False,
            "get_vni": False
        }
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an IPV6 python object from a Cumulus output command named object_04')
def create_an_ipv6_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an IPV6 object from a Cumulus output

    :param context:
    :return None:
    """

    context.object_04 = _cumulus_ipv6_converter(
        hostname="leaf03",
        plateform="linux",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_interface.json"
        ),
        filters={
            "get_loopback": True,
            "get_physical": True,
            "get_vlan": True,
            "get_peerlink": False,
            "get_vni": False
        }
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_01 should be equal to object_02')
def compare_ipv6_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_ipv6(
        host_keys=IPV6_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['leaf'],
        ipv6_host_data=context.object_01,
        ipv6_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_02 should be equal to object_03')
def compare_ipv6_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """

    assert _compare_ipv6(
        host_keys=IPV6_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['leaf'],
        ipv6_host_data=context.object_03,
        ipv6_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_01 should be equal to object_03')
def compare_ipv6_object_01_and_object_03(context) -> None:
    """
    Compare object_01 and object_03

    :param context:
    :return:
    """

    assert context.object_01 == context.object_03


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_03 should be equal to object_01')
def compare_ipv6_object_03_and_object_01(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert context.object_03 == context.object_01

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_02 should be equal to object_04')
def compare_ipv6_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """

    assert _compare_ipv6(
        host_keys=IPV6_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['leaf'],
        ipv6_host_data=context.object_04,
        ipv6_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV6 object_03 should not be equal to object_04')
def compare_ipv6_object_03_and_object_04(context) -> None:
    """
    Compare object_03 and object_04

    :param context:
    :return:
    """

    assert context.object_03 != context.object_04