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
    from functions.infos.infos_compare import _compare_infos
    from functions.infos.infos_converters import _nexus_infos_converter
    from protocols.infos import SystemInfos
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.infos")
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

########################################################################################################################
#
# Scenario
#
"""
Feature: Test protocols SystemInfos python class ./protocols/infos.py
  # Enter feature description here

  Scenario: # Enter scenario name here
    # Enter steps here
    Given I create a SystemInfos python object manually named object_01
    And I retrieve data from a YAML file to create a SystemInfos python object named object_02
    And I create a SystemInfos python object from a Nexus output command named object_03
    Then SystemInfos object_01 should be equal to object_02
    And SystemInfos object_01 should be equal to object_03
    And SystemInfos object_02 should be equal to object_03
"""
########################################################################################################################
#
# Functions
#

@given(u'I create a SystemInfos python object manually named object_01')
def create_a_sysinfos_object_manually(context) -> None:
    """
    Create a SystemInfos object manually

    :param context:
    :return None:
    """

    context.object_01 = SystemInfos(
        hostname="leaf02",
        domain="dh.local",
        version="7.0(3)I7(5a)",
        serial="96L4EUDRHHW",
        build="1.0",
        base_mac="00:00:00:00:00:01",
        memory="8129568",
        snmp_ips=["192.168.254.7", "192.168.254.17"],
        interfaces_lst=["mgmt0", "Ethernet1/1", "Ethernet1/2", "Ethernet1/3", "Ethernet1/4", "loopback0"]
    )


@given('I retrieve data from a YAML file to create a SystemInfos python object named object_02')
def create_a_sysinfos_object_from_a_json(context) -> None:
    """
    Retrieve data from a YAML file to compare with a SystemInfos object

    :param context:
    :return None:
    """

    yaml_content = open_file(
        path=f"{FEATURES_SRC_PATH}infos_tests.yml"
    )

    context.object_02 = yaml_content


@given('I create a SystemInfos python object from a Nexus output command named object_03')
def create_a_sysinfos_object_from_a_nexus_output_command(context) -> None:
    """
    Create a SystemInfos object from a Nexus output

    :param context:
    :return None:
    """

    outputs_dict = dict()

    outputs_dict[INFOS_SYS_DICT_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}nexus_show_version.json"
    )

    outputs_dict[INFOS_SNMP_DICT_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}nexus_show_snmp_host.json"
    )

    outputs_dict[INFOS_INT_DICT_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}nexus_show_ip_interface_brief.json"
    )

    outputs_dict[INFOS_DOMAIN_DICT_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}show_hostname.json"
    )

    context.object_03 = _nexus_infos_converter(
        outputs_dict
    )


@then('SystemInfos object_01 should be equal to object_02')
def compare_sysinfos_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return None:
    """

    assert _compare_infos(
        host_keys=INFOS_DATA_HOST_KEY,
        hostname="leaf02",
        infos_host_data=context.object_01,
        infos_data=context.object_02,
    )


@then('SystemInfos object_01 should be equal to object_03')
def compare_sysinfos_object_01_and_object_03(context) -> None:
    """
    Compare object_01 and object_03

    :param context:
    :return None:
    """
    assert context.object_01 == context.object_03

@then('SystemInfos object_02 should be equal to object_03')
def compare_sysinfos_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return None:
    """

    assert _compare_infos(
        host_keys=INFOS_DATA_HOST_KEY,
        hostname="leaf02",
        infos_host_data=context.object_03,
        infos_data=context.object_02,
    )