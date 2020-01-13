#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate LLDP protocols usage

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
ERROR_HEADER = "Error import [lldp_tests.py]"
HEADER = "[netests - lldp_tests.py]"
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
    from functions.discovery_protocols.lldp.lldp_converters import _juniper_lldp_converter, _cumulus_lldp_converter
    from functions.discovery_protocols.lldp.lldp_compare import _compare_lldp
    from protocols.lldp import LLDP, ListLLDP
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.lldp ")
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
@given(u'I create an LLDP python object corresponding to Juniper device manually named object_01')
def create_an_lldp_object_manually(context) -> None:
    """
    Create a LLDP object manually

    :param context:
    :return None:
    """

    lldp_neighbors_lst = ListLLDP(
        lldp_neighbors_lst=list()
    )

    lldp_neighbors_lst.lldp_neighbors_lst.append(
        LLDP(
            local_name="leaf04",
            local_port="et-0/0/0",
            neighbor_port="et-0/0/0",
            neighbor_name="router-core-01"
        )
    )

    lldp_neighbors_lst.lldp_neighbors_lst.append(
        LLDP(
            local_name="leaf04",
            local_port="et-1/3/2",
            neighbor_port="1/33",
            neighbor_name="router-no-core-01"
        )
    )

    context.object_01 = lldp_neighbors_lst

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an LLDP python object named object_02')
def create_an_lldp_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
        Retrieve data from a YAML file to compare with a LLDP object

        :param context:
        :return None:
        """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}lldp_tests.yml"
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an LLDP python object from a Juniper output command named object_03')
def create_an_lldp_object_from_a_juniper_output_command(context) -> None:
    """
    Create an LLDP object from a Juniper output

    :param context:
    :return None:
    """

    context.object_03 = _juniper_lldp_converter(
        hostname="leaf04",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}juniper_show_lldp_neighbors.json"
        )
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an LLDP python object from a Cumulus output command named object_04')
def create_an_lldp_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an LLDP object from a Juniper output

    :param context:
    :return None:
    """

    context.object_04 = _cumulus_lldp_converter (
        hostname="spine01",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_lldp_neighbors.json"
        )
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('LLDP object_01 should be equal to object_02')
def compare_lldp_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="leaf04",
        lldp_host_data=context.object_01,
        lldp_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('LLDP object_02 should be equal to object_03')
def compare_lldp_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """

    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="leaf04",
        lldp_host_data=context.object_03,
        lldp_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('LLDP object_01 should be equal to object_03')
def compare_lldp_object_01_and_object_03(context) -> None:
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
@then('LLDP object_03 should be equal to object_01')
def compare_lldp_object_03_and_object_01(context) -> None:
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
@then('LLDP object_03 should not be equal to object_04')
def compare_lldp_object_03_and_object_04(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert context.object_03 != context.object_04


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('LLDP object_02 should be equal to object_04')
def compare_lldp_object_02_and_object_04(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert _compare_lldp(
        host_keys=LLDP_DATA_HOST_KEY,
        hostname="spine01",
        lldp_host_data=context.object_04,
        lldp_yaml_data=context.object_02
    )