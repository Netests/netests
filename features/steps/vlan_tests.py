#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
This file is used for CI test to validate VLAN protocols usage

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
ERROR_HEADER = "Error import [vlan_tests.py]"
HEADER = "[netests - vlan_tests.py]"
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
    from functions.vlan.vlan_converters import _cumulus_vlan_converter, _arista_vlan_converter
    from functions.vlan.vlan_compare import _compare_vlan
    from protocols.vlan import VLAN, ListVLAN
except ImportError as importError:
    print(f"{ERROR_HEADER} protocols.vlan ")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.global_tools import open_file, open_txt_file
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.global_tools")
    print(importError)
    exit(EXIT_FAILURE)

try:
    from functions.discovery_protocols.discovery_functions import _mapping_interface_name
except ImportError as importError:
    print(f"{ERROR_HEADER} functions.discovery_protocols.discovery_functions")
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
@given(u'I create an VLAN python object corresponding to Arista device manually named object_01')
def create_an_vlan_object_manually(context) -> None:
    """
    Create a VLAN object manually

    :param context:
    :return None:
    """

    vlan_lst = ListVLAN(
        vlans_lst=list()
    )

    ports_members = list()
    for port_member in ["Ethernet4", "Ethernet5", "Ethernet6", "Ethernet7"]:
        ports_members.append(
            _mapping_interface_name(
                port_member
            )
        )

    vlan_lst.vlans_lst.append(
        VLAN(
            vlan_id="1",
            ports_members=ports_members
        )
    )

    ports_members = list()
    for port_member in ["Ethernet6"]:
        ports_members.append(
            _mapping_interface_name(
                port_member
            )
        )
    vlan_lst.vlans_lst.append(
        VLAN(
            vlan_id="1000",
            ports_members=ports_members
        )
    )

    vlan_lst.vlans_lst.append(
        VLAN(
            vlan_id="2000",
            ports_members=["eth1/6"]
        )
    )

    context.object_01 = vlan_lst

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an VLAN python object named object_02')
def create_an_vlan_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
        Retrieve data from a YAML file to compare with a VLAN object

        :param context:
        :return None:
        """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}vlan_tests.yml"
    )


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an VLAN python object from a Arista output command named object_03')
def create_an_vlan_object_from_a_arista_output_command(context) -> None:
    """
    Create an VLAN object from a Arista output

    :param context:
    :return None:
    """

    outputs_dict = dict()

    outputs_dict[VLAN_GET_L2] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}arista_show_vlan.json"
    )

    outputs_dict[VLAN_GET_L3] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}arista_show_ip_interface_vlan_1_4094.json"
    )

    outputs_dict[VLAN_GET_INT] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}arista_show_interfaces_vlan_1_4094.json"
    )

    context.object_03 = _arista_vlan_converter(
        hostname="leaf01",
        cmd_output=outputs_dict
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an VLAN python object from a Cumulus output command named object_04')
def create_an_vlan_object_from_a_cumulus_output_command(context) -> None:
    """
    Create an VLAN object from a Cumulus output

    :param context:
    :return None:
    """
    outputs_dict = dict()

    vlan_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_vrf_list.output"
    )

    if vlan_data != "":
        template = open(
            f"{TEXTFSM_PATH}cumulus_net_show_vrf_list.template")
        results_template = textfsm.TextFSM(template)

        outputs_dict[VLAN_VRF_LIST_KEY] = results_template.ParseText(vlan_data)

    outputs_dict[VLAN_VRF_DETAIL_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_interface.json"
    )

    context.object_04 = _cumulus_vlan_converter(
        hostname="leaf01",
        cmd_output=outputs_dict
    )


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('VLAN object_01 should be equal to object_02')
def compare_vlan_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_vlan(
        host_keys=VLAN_DATA_HOST_KEY,
        hostname="leaf03",
        vlan_host_data=context.object_01,
        vlan_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('VLAN object_02 should be equal to object_03')
def compare_vlan_object_02_and_object_03(context) -> None:
    """
    Compare object_02 and object_03

    :param context:
    :return:
    """

    assert _compare_vlan(
        host_keys=VLAN_DATA_HOST_KEY,
        hostname="leaf03",
        vlan_host_data=context.object_03,
        vlan_yaml_data=context.object_02
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('VLAN object_01 should be equal to object_03')
def compare_vlan_object_01_and_object_03(context) -> None:
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
@then('VLAN object_03 should be equal to object_01')
def compare_vlan_object_03_and_object_01(context) -> None:
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
@then('VLAN object_02 should be equal to object_04')
def compare_vlan_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """

    assert _compare_vlan(
        host_keys=VLAN_DATA_HOST_KEY,
        hostname="leaf01",
        vlan_host_data=context.object_04,
        vlan_yaml_data=context.object_02
    )
