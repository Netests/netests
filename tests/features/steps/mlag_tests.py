#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate MLAG protocols usage

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
ERROR_HEADER = "Error import [mlag_tests.py]"
HEADER = "[netests - mlag_tests.py]"
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
    from functions.mlag.mlag_converters import _cumulus_mlag_converter
    from functions.mlag.mlag_compare import _compare_mlag
    from protocols.mlag import MLAG
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mlag ")
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
@given(u'I create an MLAG python object corresponding to Cumulus device manually named object_01')
def create_an_mlag_object_manually(context) -> None:
    """
    Create a MLAG object manually

    :param context:
    :return None:
    """

    context.object_01 = MLAG(
        hostname="leaf01",
        local_id="50:00:00:03:00:06",
        peer_id="50:00:00:04:00:06",
        peer_alive=True,
        peer_int="peerlink.4094",
        peer_ip="169.254.1.2",
        sys_mac="44:38:39:ff:01:02",
        local_role="primary",
        peer_role="secondary",
        local_priority=100,
        peer_priority=32768,
        vxlan_anycast_ip="10.100.100.12",
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an MLAG python object named object_02')
def create_an_mlag_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
        Retrieve data from a YAML file to compare with a MLAG object

        :param context:
        :return None:
        """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}mlag_tests.yml"
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an MLAG python object from a Cumulus output command named object_03')
def create_an_mlag_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an MLAG object from a Cumulus output

    :param context:
    :return None:
    """

    context.object_03 = _cumulus_mlag_converter(
        hostname="leaf01",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_clag.json"
        )
    )


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('MLAG object_01 should be equal to object_02')
def compare_mlag_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_mlag(
        host_keys=MLAG_DATA_HOST_KEY,
        hostname="leaf01",
        mlag_host_data=context.object_01,
        mlag_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('MLAG object_01 should be equal to object_03')
def compare_mlag_object_01_and_object_03(context) -> None:
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
@then('MLAG object_03 should be equal to object_01')
def compare_mlag_object_03_and_object_01(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert context.object_03 == context.object_01