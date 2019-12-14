#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate IPV4 protocols usage

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
ERROR_HEADER = "Error import [ipv4_tests.py]"
HEADER = "[netests - ipv4_tests.py]"
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
    from functions.ip.ipv4.ipv4_converters import _cumulus_ipv4_converter
    from functions.ip.ipv4.ipv4_compare import _compare_ipv4
    from protocols.ipv4 import IPV4, ListIPV4
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ip.ipv4 ")
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
@given(u'I create an IPV4 python object corresponding to Cumulus device manually named object_01')
def create_an_ipv4_object_manually(context) -> None:
    """
    Create a IPV4 object manually

    :param context:
    :return None:
    """

    ipv4_addresses_lst = ListIPV4(
        hostname="leaf01",
        ipv4_addresses_lst=list()
    )

    ipv4_addresses_lst.ipv4_addresses_lst.append(
        IPV4(
            interface_name="eth0",
            ip_address_with_mask="10.0.4.201",
            netmask="255.255.255.0"
        )
    )

    context.object_01 = ipv4_addresses_lst

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an IPV4 python object named object_02')
def create_an_ipv4_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
        Retrieve data from a YAML file to compare with a IPV4 object

        :param context:
        :return None:
        """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}ipv4_tests.yml"
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an IPV4 python object from a Cumulus output command named object_03')
def create_an_ipv4_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an IPV4 object from a Cumulus output

    :param context:
    :return None:
    """

    context.object_03 = _cumulus_ipv4_converter(
        hostname="leaf01",
        plateform="linux",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_show_interface.json"
        ),
        get_loopback=False,
        get_physical=True,
        get_vni=False,
        get_peerlink=False,
        get_vlan=False
    )


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV4 object_01 should be equal to object_02')
def compare_ipv4_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_ipv4(
        host_keys=IPV4_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['leaf'],
        ipv4_host_data=context.object_01,
        ipv4_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV4 object_01 should be equal to object_03')
def compare_ipv4_object_01_and_object_03(context) -> None:
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
@then('IPV4 object_03 should be equal to object_01')
def compare_ipv4_object_03_and_object_01(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert context.object_03 == context.object_01