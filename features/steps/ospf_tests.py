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

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given(u'I create an OSPF python object corresponding to Cumulus device manually named object_01')
def create_an_ospf_object_manually(context) -> None:
    """
    Create a OSPF object manually

    :param context:
    :return None:
    """

    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    ### VRF - Default
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ###### Area 0.0.0.0
    ospf_session_lst = ListOSPFSessions(
        ospf_sessions_lst=list()
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            hostname="spine01",
            peer_rid="10.255.255.203",
            peer_ip="10.1.3.2",
            local_interface="swp3",
            session_state="Full"
        )
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            hostname="spine01",
            peer_rid="10.255.255.204",
            peer_ip="10.1.4.2",
            local_interface="swp4",
            session_state="Full"
        )
    )

    ospf_area_lst.ospf_sessions_area_lst.append(
        OSPFSessionsArea(
            area_number="0.0.0.0",
            ospf_sessions=ospf_session_lst
        )
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="default",
            router_id="10.255.255.101",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )

    ### VRF - Default
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ###### Area 0.0.0.100
    ospf_session_lst = ListOSPFSessions(
        ospf_sessions_lst=list()
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            hostname="spine01",
            peer_rid="201.201.201.201",
            peer_ip="10.0.5.201",
            local_interface="eth0",
            session_state="Full"
        )
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            hostname="spine01",
            peer_rid="205.205.205.205",
            peer_ip="10.0.5.205",
            local_interface="eth0",
            session_state="Full"
        )
    )

    ospf_area_lst.ospf_sessions_area_lst.append(
        OSPFSessionsArea(
            area_number="0.0.0.100",
            ospf_sessions=ospf_session_lst
        )
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="mgmt",
            router_id="10.0.5.101",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )

    context.object_01 = OSPF(
        hostname="spine01",
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I retrieve data from a YAML file corresponding to devices to create an OSPF python object named object_02')
def create_an_ospf_object_from_a_yaml_corresponding_to_cumulus(context) -> None:
    """
    Retrieve data from a YAML file to compare with a OSPF object

    :param context:
    :return None:
    """

    context.object_02 = open_file(
        path=f"{FEATURES_SRC_PATH}ospf_tests.yml"
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
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

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an OSPF python object from a Juniper output command named object_04')
def create_an_ospf_object_from_a_juniper_output_command(context) -> None:
    """
    Create an OSPF object from a Juniper output

    :param context:
    :return None:
    """
    outputs_dict = dict()

    outputs_dict['default'] = dict()
    outputs_dict['default'][OSPF_NEI_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}juniper_show_ospf_neighbor_detail.json"
    )

    outputs_dict['default'][OSPF_RIB_KEY] = open_file(
        path=f"{FEATURES_OUTPUT_PATH}juniper_show_ospf_overview.json"
    )

    context.object_04 = _juniper_ospf_converter(
        hostname="leaf04",
        cmd_outputs=outputs_dict
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an OSPF python object from a Extreme VSP output command named object_05')
def create_an_ospf_object_from_a_extreme_vsp_output_command(context) -> None:
    """
    Create an OSPF object from a Extreme VSP output

    :param context:
    :return None:
    """

    outputs_dict = dict()
    outputs_dict['default'] = dict()

    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_ospf_neighbor.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_neighbor.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict['default'][OSPF_NEI_KEY] = parsed_results


    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_ospf_interface.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf_interface.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict['default'][OSPF_INT_KEY] = parsed_results

    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_ospf.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_ospf.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict['default'][OSPF_RIB_KEY] = parsed_results

    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_interface.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_interface.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict['default'][OSPF_INT_NAME_KEY] = parsed_results

    context.object_05 = _extreme_vsp_ospf_converter(
        hostname="spine02",
        cmd_outputs=outputs_dict
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@given('I create an OSPF python object from a Cisco IOS output command named object_06')
def create_an_ospf_object_from_a_cisco_ios_output_command(context) -> None:
    """
    Create an OSPF object from a Cisco IOS output

    :param context:
    :return None:
    """

    outputs_dict = dict()

    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cisco_ios_show_ip_ospf.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict[OSPF_RIB_KEY] = parsed_results


    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cisco_ios_show_ip_ospf_neighbor_detail.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf_neighbor_detail.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict[OSPF_NEI_KEY] = parsed_results

    ospf_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}cisco_ios_show_ip_ospf_interface_brief.output"
    )

    if ospf_data != "":
        template = open(
            f"{TEXTFSM_PATH}cisco_ios_show_ip_ospf_interface_brief.template")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(ospf_data)

        outputs_dict[OSPF_INT_KEY] = parsed_results

    context.object_06 = _ios_ospf_converter(
        hostname="leaf05",
        cmd_outputs=outputs_dict
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_01 should be equal to object_02')
def compare_ospf_object_01_and_object_02(context) -> None:
    """
    Compare object_01 and object_02

    :param context:
    :return:
    """

    assert _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname="spine01",
        ospf_host_data=context.object_01,
        ospf_yaml_data=context.object_02,
        level_test=0
    )


# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_01 should be equal to object_03')
def compare_ospf_object_01_and_object_03(context) -> None:
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
@then('OSPF object_03 should be equal to object_01')
def compare_ospf_object_03_and_object_01(context) -> None:
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

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_02 should be equal to object_04')
def compare_ospf_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """
    assert _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname="leaf04",
        ospf_host_data=context.object_04,
        ospf_yaml_data=context.object_02,
        level_test=0
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_02 should be equal to object_05')
def compare_ospf_object_02_and_object_05(context) -> None:
    """
    Compare object_02 and object_05

    :param context:
    :return:
    """
    assert _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname="spine02",
        ospf_host_data=context.object_05,
        ospf_yaml_data=context.object_02,
        level_test=0
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_02 should be equal to object_06')
def compare_ospf_object_02_and_object_06(context) -> None:
    """
    Compare object_02 and object_06

    :param context:
    :return:
    """

    assert _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname="leaf05",
        ospf_host_data=context.object_06,
        ospf_yaml_data=context.object_02,
        level_test=0
    )

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_03 should not be equal to object_04')
def compare_ospf_object_03_and_object_04(context) -> None:
    """
    Compare object_03 and object_04

    :param context:
    :return:
    """

    assert context.object_03 != context.object_04

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_03 should not be equal to object_05')
def compare_ospf_object_03_and_object_05(context) -> None:
    """
    Compare object_03 and object_05

    :param context:
    :return:
    """

    assert context.object_03 != context.object_05

# ----------------------------------------------------------------------------------------------------------------------
#
#
#
@then('OSPF object_03 should not be equal to object_06')
def compare_ospf_object_03_and_object_06(context) -> None:
    """
    Compare object_03 and object_06

    :param context:
    :return:
    """

    assert context.object_03 != context.object_06