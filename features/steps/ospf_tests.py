#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate OSPF protocols usage

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
ERROR_HEADER = "Error import [ospf_tests.py]"
HEADER = "[netests - ospf_tests.py]"
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
    from functions.ospf.ospf_converters import _extreme_vsp_ospf_converter, _juniper_ospf_converter
    from functions.ospf.ospf_converters import _ios_ospf_converter, _cumulus_ospf_converter
    from functions.ospf.ospf_compare import _compare_ospf
    from protocols.ospf import OSPF, ListOSPFSessionsVRF, OSPFSessionsVRF, ListOSPFSessionsArea, OSPFSessionsArea
    from protocols.ospf import ListOSPFSessions, OSPFSession
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.ospf ")
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

@given(u'I create an OSPF python object corresponding to Cumulus device manually named object_01')
def create_an_ospf_object_manually(context) -> None:
    """
    Create a OSPF object manually

    :param context:
    :return None:
    """
    pass

@given('I retrieve data from a YAML file corresponding to Cumulus device to create an OSPF python object named object_02')
def create_an_ospf_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
    Retrieve data from a YAML file to compare with a OSPF object

    :param context:
    :return None:
    """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}ospf_tests_cumulus.yml"
    )


@given('I create an OSPF python object from a Cumulus output command named object_03')
def create_an_ospf_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an OSPF object from a Cumulus output

    :param context:
    :return None:
    """
    outputs_lst = list()

    # VRF - Default
    data = dict()

    data['rid'] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_ospf.json"
    )

    data['data'] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_ospf_neighbor_detail.json"
    )

    outputs_lst.append(data)

    # VRF - mgmt
    data = dict()

    data['rid'] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_ospf_vrf.json"
    )

    data['data'] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_ospf_vrf_neighbor_detail.json"
    )

    outputs_lst.append(data)


    context.object_03 = _cumulus_ospf_converter(
        hostname="spine01",
        cmd_outputs=outputs_lst
    )

    print(context.object_03)

@given('I retrieve data from a YAML file corresponding to Juniper device to create an OSPF python object named object_04')
def create_an_ospf_object_from_a_yaml_corresponding_to_juniper(context) -> None:
    """
    Retrieve data from a YAML file to compare with a OSPF object

    :param context:
    :return None:
    """
    pass

@given('I create an OSPF python object from a Juniper output command named object_05')
def create_an_ospf_object_from_a_juniper_output_command(context) -> None:
    """
    Create an OSPF object from a Juniper output

    :param context:
    :return None:
    """
    pass

@given('I retrieve data from a YAML file corresponding to Extreme VSP device to create an OSPF python object named object_06')
def create_an_ospf_object_from_a_yaml_corresponding_to_extreme_vsp(context) -> None:
    """
    Retrieve data from a YAML file to compare with a OSPF object

    :param context:
    :return None:
    """
    pass

@given('I create an OSPF python object from a Extreme VSP output command named object_07')
def create_an_ospf_object_from_a_extreme_vsp_output_command(context) -> None:
    """
    Create an OSPF object from a Extreme VSP output

    :param context:
    :return None:
    """
    pass

@given('I retrieve data from a YAML file corresponding to Cisco IOS device to create an OSPF python object named object_08')
def create_an_ospf_object_from_a_yaml_corresponding_to_cisco_ios(context) -> None:
    """
    Retrieve data from a YAML file to compare with a OSPF object

    :param context:
    :return None:
    """
    pass

@given('I create an OSPF python object from a Cisco IOS output command named object_09')
def create_an_ospf_object_from_a_cisco_ios_output_command(context) -> None:
    """
    Create an OSPF object from a Cisco IOS output

    :param context:
    :return None:
    """
    pass


@then('OSPF object_01 should be equal to object_02')
def compare_ospf_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """
    pass

@then('OSPF object_01 should be equal to object_03')
def compare_ospf_object_01_and_object_03(context) -> None:
    """
    Compare object_01 and object_03

    :param context:
    :return:
    """
    pass

@then('OSPF object_02 should be equal to object_03')
def compare_ospf_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """
    assert _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname="spine01",
        ospf_host_data=context.object_03,
        ospf_yaml_data=context.object_02,
        level_test=0
    )

@then('OSPF object_04 should be equal to object_05')
def compare_ospf_object_04_and_object_05(context) -> None:
    """
    Compare object_04 and object_05

    :param context:
    :return:
    """
    pass

@then('OSPF object_05 should be equal to object_04')
def compare_ospf_object_05_and_object_04(context) -> None:
    """
    Compare object_05 and object_04

    :param context:
    :return:
    """
    pass

@then('OSPF object_06 should be equal to object_07')
def compare_ospf_object_06_and_object_07(context) -> None:
    """
    Compare object_06 and object_07

    :param context:
    :return:
    """
    pass

@then('OSPF object_07 should be equal to object_06')
def compare_ospf_object_07_and_object_06(context) -> None:
    """
    Compare object_07 and object_06

    :param context:
    :return:
    """
    pass

@then('OSPF object_08 should be equal to object_09')
def compare_ospf_object_08_and_object_09(context) -> None:
    """
    Compare object_08 and object_09

    :param context:
    :return:
    """
    pass

@then('OSPF object_09 should be equal to object_08')
def compare_ospf_object_09_and_object_08(context) -> None:
    """
    Compare object_09 and object_08

    :param context:
    :return:
    """
    pass

@then('OSPF object_02 should not be equal to object_04')
def compare_ospf_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """
    pass

@then('OSPF object_04 should not be equal to object_06')
def compare_ospf_object_04_and_object_06(context) -> None:
    """
    Compare object_04 and object_06

    :param context:
    :return:
    """
    pass

@then('OSPF object_06 should not be equal to object_08')
def compare_ospf_object_06_and_object_08(context) -> None:
    """
    Compare object_06 and object_08

    :param context:
    :return:
    """
    pass