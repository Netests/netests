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
    from functions.ip.ipv4.ipv4_converters import _cumulus_ipv4_converter, _nexus_ipv4_converter, _arista_ipv4_converter
    from functions.ip.ipv4.ipv4_converters import _ios_ipv4_converter
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
@given('I create an IPV4 python object from a Cisco Nexus output command named object_04')
def create_an_ipv4_object_from_a_nexus_output_command(context) -> None:
    """
    Create an IPV4 object from a Cisco Nexus output

    :param context:
    :return None:
    """

    outputs_lst = list()

    outputs_lst.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}nexus_show_ip_interface.json"
        )
    )

    data = open_file(
            path=f"{FEATURES_OUTPUT_PATH}nexus_show_ip_interface_vrf_client_00.json"
        )

    if data != "" and data is not None:
        outputs_lst.append(data)

    outputs_lst.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}nexus_show_ip_interface_vrf_management.json"
        )
    )

    outputs_lst.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}nexus_show_ip_interface_vrf_test_dylan.json"
        )
    )

    context.object_04 = _nexus_ipv4_converter(
        hostname="leaf01",
        plateform="nxos",
        cmd_outputs=outputs_lst,
        get_loopback=False,
        get_physical=False,
        get_vni=False,
        get_peerlink=False,
        get_vlan=True
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an IPV4 python object from a Arista output command named object_05')
def create_an_ipv4_object_from_a_arista_output_command(context) -> None:
    """
    Create an IPV4 object from a Arista output

    :param context:
    :return None:
    """

    context.object_05 = _arista_ipv4_converter(
        hostname="leaf03",
        plateform="eos",
        cmd_output=open_file(
            path=f"{FEATURES_OUTPUT_PATH}arista_show_ip_interface.json"
        ),
        get_loopback=True,
        get_physical=True,
        get_vni=False,
        get_peerlink=False,
        get_vlan=True
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an IPV4 python object from a Cisco IOS output command named object_06')
def create_an_ipv4_object_from_a_ios_output_command(context) -> None:
    """
    Create an IPV4 object from a Cisco IOS output

    :param context:
    :return None:
    """

    ipv4_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cisco_ios_show_ip_interface.output"
    )

    if ipv4_data != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_interface.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ipv4_data)

    context.object_06 = _ios_ipv4_converter(
        hostname="leaf05",
        plateform="ios",
        cmd_output=parsed_results,
        get_loopback=True,
        get_physical=False,
        get_vni=False,
        get_peerlink=False,
        get_vlan=True
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
@then('IPV4 object_02 should be equal to object_03')
def compare_ipv4_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """

    assert _compare_ipv4(
        host_keys=IPV4_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['leaf'],
        ipv4_host_data=context.object_03,
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

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV4 object_02 should be equal to object_04')
def compare_ipv4_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """

    assert _compare_ipv4(
        host_keys=IPV4_DATA_HOST_KEY,
        hostname="leaf02",
        groups=['leaf'],
        ipv4_host_data=context.object_04,
        ipv4_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV4 object_02 should be equal to object_05')
def compare_ipv4_object_02_and_object_05(context) -> None:
    """
    Compare object_02 and object_05

    :param context:
    :return:
    """

    assert _compare_ipv4(
        host_keys=IPV4_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['leaf'],
        ipv4_host_data=context.object_05,
        ipv4_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('IPV4 object_02 should be equal to object_06')
def compare_ipv4_object_02_and_object_06(context) -> None:
    """
    Compare object_02 and object_06

    :param context:
    :return:
    """

    print(context.object_06)

    assert _compare_ipv4(
        host_keys=IPV4_DATA_HOST_KEY,
        hostname="leaf05",
        groups=['leaf'],
        ipv4_host_data=context.object_06,
        ipv4_yaml_data=context.object_02
    )