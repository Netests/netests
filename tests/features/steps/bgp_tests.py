#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import json
import yaml
import textfsm
from behave import given, when, then
from const.constants import NOT_SET, FEATURES_SRC_PATH, FEATURES_OUTPUT_PATH, TEXTFSM_PATH, BGP_SESSIONS_HOST_KEY
from functions.bgp.bgp_compare import _compare_bgp
from functions.global_tools import open_file, open_txt_file
from functions.bgp.bgp_converters import (
    _cumulus_bgp_converter,
    _generic_state_converter
)
from functions.bgp.bgp_converters import (
    _extreme_vsp_bgp_converter,
    _extreme_vsp_peer_uptime_converter
)
from protocols.bgp import (
    BGP,
    ListBGPSessionsVRF,
    BGPSessionsVRF,
    ListBGPSessions,
    BGPSession
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


@given(u'I create a BGP python object manually named object_01')
def step_impl(context) -> None:
    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )
    bgp_sessions_lst = ListBGPSessions(
        list()
    )
    bgp_sessions_lst.bgp_sessions.append(
        BGPSession(
            src_hostname="spine01",
            peer_ip="10.2.5.2",
            peer_hostname=NOT_SET,
            remote_as="65205",
            state_brief=_generic_state_converter(
                "Established"
            ),
            session_state="Established",
            state_time=_extreme_vsp_peer_uptime_converter(
                day="0",
                hour="01",
                min="05",
                sec="26"
            ),
            prefix_received=NOT_SET
        )
    )
    bgp_sessions_lst.bgp_sessions.append(
        BGPSession(
            src_hostname="spine01",
            peer_ip="10.255.255.205",
            peer_hostname=NOT_SET,
            remote_as="65205",
            state_brief=_generic_state_converter(
                "Established"
            ),
            session_state="Established",
            state_time=_extreme_vsp_peer_uptime_converter(
                day="0",
                hour="01",
                min="05",
                sec="26"
            ),
            prefix_received=NOT_SET
        )
    )
    bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
        BGPSessionsVRF(
            vrf_name="default",
            as_number="65100",
            router_id="10.255.255.102",
            bgp_sessions=bgp_sessions_lst
        )
    )
    bgp_sessions_lst = ListBGPSessions(
        list()
    )
    bgp_sessions_lst.bgp_sessions.append(
        BGPSession(
            src_hostname="spine01",
            peer_ip="10.0.5.202",
            peer_hostname=NOT_SET,
            remote_as="65202",
            state_brief=_generic_state_converter(
                "Idle"
            ),
            session_state="Idle",
            state_time=_extreme_vsp_peer_uptime_converter(
                day="16",
                hour="1",
                min="04",
                sec="10"
            ),
            prefix_received=NOT_SET
        )
    )
    bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
        BGPSessionsVRF(
            vrf_name="tenant01",
            as_number="65100",
            router_id="10.0.5.102",
            bgp_sessions=bgp_sessions_lst
        )
    )
    context.object_01 = BGP(
        hostname="spine01",
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )


@given(u'I print it with __repr__ and in JSON format')
def step_impl(context):
    PP.pprint(context.object_01.to_json())
    print(context.object_01)


@given('I retrieve data from a YAML file to create a BGP python object named object_02')
def create_a_bgp_object_from_a_yaml(context) -> None:
    """
    Retrieve data from a YAML file to compare with a BGP object

    :param context:
    :return None:
    """

    context.object_02  = open_file(
        path=f"{FEATURES_SRC_PATH}bgp_tests.yml"
    )


@given('I create a BGP python object from a Extreme VSP output command named object_03')
def create_a_bgp_object_from_a_extreme_vsp_output_command(context) -> None:
    """
    Create a BGP object from a Extreme VSP output

    :param context:
    :return None:
    """

    outputs_dict = dict()

    ######### VRF - default
    bgp_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_bgp_summary.output"
    )

    if bgp_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_bgp_summary.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(bgp_data)

        outputs_dict['default'] = parsed_results

    ######### VRF - tenant01
    bgp_data = open_txt_file(
        path=f"{FEATURES_OUTPUT_PATH}extreme_vsp_show_ip_bgp_summary_vrf.output"
    )

    if bgp_data != "":
        template = open(
            f"{TEXTFSM_PATH}extreme_vsp_show_ip_bgp_summary.textfsm")
        results_template = textfsm.TextFSM(template)

        parsed_results = results_template.ParseText(bgp_data)

        outputs_dict['tenant01'] = parsed_results

    context.object_03 = _extreme_vsp_bgp_converter(
        hostname="spine01",
        cmd_outputs=outputs_dict
    )


@given('I create a BGP python object from a Cumulus output command named object_04')
def create_a_bgp_object_from_a_cumulus_output_command(context) -> None:
    """
    Create a BGP object from a Cumulus output

    :param context:
    :return None:
    """

    cmd_outputs = list()

    cmd_outputs.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_bgp_summary.json"
        )
    )

    cmd_outputs.append(
        open_file(
            path=f"{FEATURES_OUTPUT_PATH}cumulus_net_show_bgp_vrf_summary.json"
        )
    )

    context.object_04 = _cumulus_bgp_converter(
        hostname="spine01",
        cmd_outputs=cmd_outputs
    )


@then('BGP object_01 should be equal to object_03')
def compare_bgp_object_01_and_object_03(context) -> None:
    """
    Compare object_01 and object_03

    :param context:
    :return:
    """

    assert context.object_01 == context.object_03


@then('BGP object_03 should be equal to object_01')
def compare_bgp_object_03_and_object_01(context) -> None:
    """
    Compare object_03 and object_01

    :param context:
    :return:
    """

    assert context.object_03 == context.object_01


@then('BGP object_02 should be equal to object_04')
def compare_bgp_object_02_and_object_04(context) -> None:
    """
    Compare object_02 and object_04

    :param context:
    :return:
    """

    assert _compare_bgp(
        host_keys=BGP_SESSIONS_HOST_KEY,
        hostname="spine01",
        bgp_host_data=context.object_04,
        bgp_yaml_data=context.object_02
    )

@then('BGP object_03 should be not equal to object_04')
def compare_bgp_object_03_and_object_04(context) -> None:
    """
    Compare object_03 and object_04

    :param context:
    :return:
    """

    assert context.object_03 != context.object_04


@then('BGP object_04 should be not equal to object_03')
def compare_bgp_object_04_and_object_03(context) -> None:
    """
    Compare object_04 and object_03

    :param context:
    :return:
    """

    assert context.object_04 != context.object_03
