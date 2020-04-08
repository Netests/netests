#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
import textfsm
from const.constants import (
    NOT_SET,
    FEATURES_SRC_PATH,
    FEATURES_OUTPUT_PATH,
    VRF_DATA_KEY
)
from functions.vrf.vrf_compare import _compare_vrf
from functions.vrf.juniper.netconf.converter import (
    _juniper_vrf_netconf_converter
)
from functions.vrf.cumulus.api.converter import _cumulus_vrf_api_converter
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import (
    open_file,
    open_txt_file,
    open_txt_file_as_bytes
)
from behave import given, when, then


@given(u'I create a VRF object equals to Juniper manually named o01')
def step_impl(context):
    context.o01 = ListVRF(
        vrf_lst=list()
    )

    context.o01.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="1.1.1.1",
            vrf_type="forwarding",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o01.vrf_lst.append(
        VRF(
            vrf_name="INTERNAL_PEERING_VRF",
            vrf_id="0.0.0.0",
            vrf_type="non-forwarding",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o01.vrf_lst.append(
        VRF(
            vrf_name="mgmt_junos",
            vrf_id="0.0.0.0",
            vrf_type="forwarding",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I open YAML to create a VRF object equals to Juniper named o02')
def step_impl(context):
    context.o02 = open_file(
        path=(
            f"{FEATURES_SRC_PATH}vrf_tests.yml"
        )
    )


@given(u'I create a VRF object from a Juniper Netconf output named o03')
def step_impl(context):
    context.o03 = _juniper_vrf_netconf_converter(
        hostname="leaf04",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/juniper/netconf/"
                "get_instance_information_details.xml"
            )
        )
    )


@given(u'I create a VRF object equals to Cumulus manually named o04')
def step_impl(context):
    context.o04 = ListVRF(
        vrf_lst=list()
    )

    context.o04.vrf_lst.append(
        VRF(
            vrf_name="mgmt",
            vrf_id="1001",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a Cumulus API output named o05')
def step_impl(context):
    context.o05 = _cumulus_vrf_api_converter(
        hostname="leaf01",
        cmd_output=open_txt_file_as_bytes(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/cumulus/api/"
                "cumulus_http_show_vrf.txt"
            )
        )
    )


@given(u'I create a VRF object from a Cumulus SSH output named o06')
def step_impl(context):
    context.o06 = _cumulus_vrf_ssh_converter(
        hostname="leaf01",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/cumulus/ssh/"
                "cumulus_net_show_vrf.txt"
            )
        )
    )


@then(u'VRF object_01 should be equal to object_02')
def step_impl(context):

    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o01,
        vrf_yaml_data=context.o02
    )


@then(u'VRF object_01 should be equal to object_03')
def step_impl(context):
    assert context.o01 == context.o03


@then(u'VRF object_02 should be not equal to object_03')
def step_impl(context):
    
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o03,
        vrf_yaml_data=context.o02
    )


@then(u'VRF object_02 should be not equal to object_04')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o04,
        vrf_yaml_data=context.o02
    )


@then(u'VRF object_02 should be not equal to object_05')
def step_impl(context):
    print(context.o05)
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o05,
        vrf_yaml_data=context.o02
    )


@then(u'VRF object_02 should be not equal to object_06')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o06,
        vrf_yaml_data=context.o02
    )


@then(u'VRF object_04 should be not equal to object_05')
def step_impl(context):
    assert context.o04 == context.o05


@then(u'VRF object_04 should be not equal to object_06')
def step_impl(context):
    assert context.o04 == context.o06
