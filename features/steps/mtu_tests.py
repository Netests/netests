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
ERROR_HEADER = "Error import [mtu_tests.py]"
HEADER = "[netests - mtu_tests.py]"
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
    from protocols.mtu import InterfaceMTU, ListInterfaceMTU, MTU
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mtu")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.mtu.mtu_compare import _compare_mtu
    from functions.mtu.mtu_converters import _ios_mtu_converter, _cumulus_mtu_converter
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.mtu")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
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
# Scenario
#

"""
Feature: Test protocols MTU python class ./protocols/mtu.py
  Scenario: Create two MTU objects
    Given I create a MTU object with 4 interfaces named object_01
    And a JSON object with data to create a MTU object named object_02
    And a MTU object retrieve on a network device named object_03
    Then object_01 should be equal to object_02
    And object_03 should be equal to a MTU defintion describe in verity file
"""
########################################################################################################################
#
# Functions
#

@given(u'I create a MTU object with {nb_int_01:d} interfaces named object_01')
def step_impl(context, nb_int_01):
    """
    Create a MTU object and store it in context object.

    :param context:
    :param nb_int_01:
    :return None:
    """

    i = 0
    interface_mtu_lst = ListInterfaceMTU(
        list()
    )

    while i < nb_int_01:

        interface_mtu_lst.interface_mtu_lst.append(
            InterfaceMTU(
                interface_name=_mapping_interface_name(
                    f"Gi0/{i}"
                ),
                mtu_size=(2000+(200*i)),
            )
        )

        i += 1

    context.object_01 = MTU(
        hostname="spine01",
        mtu_global=1500,
        interface_mtu_lst=interface_mtu_lst
    )


@given('a JSON object with data to create a MTU object named object_02')
def create_a_mtu_object_from_a_json(context) -> None:
    """
    JSON file data structure must be as follow:

    spine01:
      global_mtu: 1500
      interfaces:
        lo0: 1514

    :param context:
    :param mtu_data: Data to create a MTU object
    :param hostname: Device hostname
    :return:
    """

    mtu_data = open_file(
        path=f"{FEATURES_SRC_PATH}mtu_tests.yml"
    )

    hostname = list(mtu_data.keys())[0]

    interface_mtu_lst = ListInterfaceMTU(
        list()
    )

    if hostname in mtu_data.keys():
        if MTU_INTER_YAML_KEY in mtu_data.get(hostname):
            for interface_name in mtu_data.get(hostname).get(MTU_INTER_YAML_KEY):
                interface_mtu_lst.interface_mtu_lst.append(
                    InterfaceMTU(
                        interface_name=_mapping_interface_name(
                            interface_name
                        ),
                        mtu_size=mtu_data.get(hostname).get(MTU_INTER_YAML_KEY).get(interface_name, NOT_SET)
                    )
                )

        context.object_02 = MTU(
            hostname=hostname,
            mtu_global=mtu_data.get(hostname).get(MTU_GLOBAL_YAML_KEY, NOT_SET),
            interface_mtu_lst=interface_mtu_lst
        )


@given('a MTU object retrieve on a network device named object_03')
def create_a_mtu_object_from_a_network_device(context) -> None:
    """
    Create a MTU protocols object from a network devices

    :param context:
    :return:
    """

    mtu_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cisco_ios_show_interfaces.output"
    )

    if mtu_data != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_interface.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(mtu_data)

    context.object_03 = _ios_mtu_converter(
        hostname="spine01",
        cmd_output=parsed_results
    )

@given('I create a MTU python object from a Cumulus output command named object_04')
def create_a_mtu_object_from_a_cumulus_output_command(context) -> None:
    """
    Create a MTU object from a Cumulus Linux output

    :param context:
    :return None:
    """

    context.object_04 = _cumulus_mtu_converter(
        hostname="spine01",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_inteface_all.json"
        )
    )


@then('object_01 should be equal to object_02')
def compare_mtu_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """
    assert context.object_01 == context.object_02


@then('object_03 should be equal to a MTU defintion describe in verity file')
def compare_mtu_object_01_and_json_object(context) -> None:
    """
    Compate object based on a verity file

    :param context:
    :param mtu_data:
    :param hostname:
    :return:
    """
    mtu_data = open_file(
        path=f"{FEATURES_SRC_PATH}mtu_tests_validate.yml"
    )
    hostname = list(mtu_data.keys())[0]

    assert _compare_mtu(
        hostname=hostname,
        mtu_host_data=context.object_03,
        mtu_yaml_data=mtu_data
    )

@then('MTU object_02 should not be equal to object_04')
def compare_mtu_object_02_and_object_04(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """
    assert (context.object_02 != context.object_04)