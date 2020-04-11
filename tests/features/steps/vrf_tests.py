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
from functions.vrf.extreme_vsp.ssh.converter import _extreme_vsp_vrf_ssh_converter
from functions.vrf.ios.ssh.converter import _ios_vrf_ssh_converter
from functions.vrf.iosxr.ssh.converter import _iosxr_vrf_ssh_converter
from functions.vrf.iosxr.netconf.converter import _iosxr_vrf_netconf_converter
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


@given(u'I create a VRF object equals to IOS-XR manually named o07')
def step_impl(context):
    context.o07 = ListVRF(
        vrf_lst=list()
    )

    context.o07.vrf_lst.append(
        VRF(
            vrf_name="EXTERNAL_PEERING",
            vrf_id=NOT_SET,
            vrf_type="Regular",
            l3_vni=NOT_SET,
            rd="65000:100",
            rt_imp="65000:1",
            rt_exp="65000:1",
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o07.vrf_lst.append(
        VRF(
            vrf_name="MGMT_VRF",
            vrf_id=NOT_SET,
            vrf_type="Regular",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS-XR SSH output named o08')
def step_impl(context):
    context.o08 = _iosxr_vrf_ssh_converter(
        hostname="spine03",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/ssh/"
                "cisco_iosxr_show_vrf_all_detail.txt"
            )
        )
    )


@given(u'I create a VRF object from a IOS-XR Netconf output named o09')
def step_impl(context):
    config = dict()
    config['VRF'] = open_txt_file(
        path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
                "cisco_iosxr_nc_get_vrf.xml"
            )
    )
    config['BGP'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_bgp.xml"
        )
    )

    context.o09 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object equals IOS-XR multi manually output named o10')
def step_impl(context):
    context.o10 = ListVRF(
        vrf_lst=list()
    )

    context.o10.vrf_lst.append(
        VRF(
            vrf_name="EXTERNAL_PEERING",
            vrf_id=NOT_SET,
            vrf_type="Regular",
            l3_vni=NOT_SET,
            rd="65000:100",
            rt_imp="65000:1",
            rt_exp="65000:1",
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o10.vrf_lst.append(
        VRF(
            vrf_name="MGMT_VRF",
            vrf_id=NOT_SET,
            vrf_type="Regular",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o10.vrf_lst.append(
        VRF(
            vrf_name="INTERNAL_PEERING",
            vrf_id=NOT_SET,
            vrf_type="Regular",
            l3_vni=NOT_SET,
            rd="65000:200",
            rt_imp="65000:2",
            rt_exp="65000:2",
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS-XR multi Netconf output named o11')
def step_impl(context):
    config = dict()
    config['VRF'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_vrf2.xml"
        )
    )
    config['BGP'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_bgp2.xml"
        )
    )

    context.o11 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object equals to Extreme VSP manually named o12')
def step_impl(context):
    context.o12 = ListVRF(
        vrf_lst=list()
    )

    context.o12.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="0",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o12.vrf_lst.append(
        VRF(
            vrf_name="mgmt_vrf",
            vrf_id="1",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o12.vrf_lst.append(
        VRF(
            vrf_name="mgmt",
            vrf_id="512",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a Extreme VSP SSH output named o13')
def step_impl(context):
    context.o13 = _extreme_vsp_vrf_ssh_converter(
        hostname="spine02",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/extreme_vsp/ssh/"
                "extreme_vsp_show_ip_vrf.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS manually named o14')
def step_impl(context):
    context.o14 = ListVRF(
        vrf_lst=list()
    )

    context.o14.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="0",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o14.vrf_lst.append(
        VRF(
            vrf_name="MGMT_VRF",
            vrf_id="1",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd='65000:999',
            rt_imp='65100:9',
            rt_exp='65100:9',
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o14.vrf_lst.append(
        VRF(
            vrf_name="SECURE_ZONE",
            vrf_id="2",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS SSH output named o15')
def step_impl(context):
    context.o15 = _ios_vrf_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/ssh/"
                "cisco_ios_show_ip_vrf_detail.txt"
            )
        )
    )

@then(u'VRF object_01 should be equal to YAML file')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o01,
        test=True
    )


@then(u'VRF object_01 should be equal to object_03')
def step_impl(context):
    assert context.o01 == context.o03


@then(u'VRF YAML file should be equal to object_03')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o03,
        test=True
    )


@then(u'VRF YAML file should be equal to object_04')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o04,
        test=True
    )


@then(u'VRF YAML file should be equal to object_05')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o05,
        test=True
    )


@then(u'VRF YAML file should be equal to object_06')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o06,
        test=True
    )


@then(u'VRF object_04 should be equal to object_05')
def step_impl(context):
    assert context.o04 == context.o05


@then(u'VRF object_04 should be equal to object_06')
def step_impl(context):
    assert context.o04 == context.o06


@then(u'VRF YAML file should be equal to object_07')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine03",
        groups=['iosxr'],
        vrf_host_data=context.o07,
        test=True
    )


@then(u'VRF YAML file should be equal to object_08')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine03",
        groups=['iosxr'],
        vrf_host_data=context.o08,
        test=True
    )


@then(u'VRF object_07 should be equal to object_08')
def step_impl(context):
    assert context.o07 == context.o08


@then(u'VRF YAML file should be equal to object_09')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine03",
        groups=['iosxr'],
        vrf_host_data=context.o09,
        test=True
    )


@then(u'VRF object_07 should be equal to object_09')
def step_impl(context):
    assert context.o07 == context.o09


@then(u'VRF object_08 should be equal to object_09')
def step_impl(context):
    assert context.o08 == context.o09


@then(u'VRF object_10 should be equal to object_11')
def step_impl(context):
    assert context.o10 == context.o11


@then(u'VRF object_12 should be equal to object_13')
def step_impl(context):
    assert context.o12== context.o13


@then(u'VRF YAML file should be equal to object_12')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine02",
        groups=['extreme_vsp'],
        vrf_host_data=context.o12,
        test=True
    )


@then(u'VRF YAML file should be equal to object_13')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine02",
        groups=['extreme_vsp'],
        vrf_host_data=context.o13,
        test=True
    )


@then(u'VRF object_14 should be equal to object_15')
def step_impl(context):
    assert context.o14 == context.o15


@then(u'VRF YAML file should be equal to object_14')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf05",
        groups=['ios'],
        vrf_host_data=context.o14,
        test=True
    )


@then(u'VRF YAML file should be equal to object_15')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf05",
        groups=['ios'],
        vrf_host_data=context.o15,
        test=True
    )
