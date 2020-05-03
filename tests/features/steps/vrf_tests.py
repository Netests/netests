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
from functions.vrf.arista.api.converter import _arista_vrf_api_converter
from functions.vrf.arista.netconf.converter import _arista_vrf_netconf_converter
from functions.vrf.arista.ssh.converter import _arista_vrf_ssh_converter
from functions.vrf.cumulus.api.converter import _cumulus_vrf_api_converter
from functions.vrf.cumulus.ssh.converter import _cumulus_vrf_ssh_converter
from functions.vrf.extreme_vsp.ssh.converter import _extreme_vsp_vrf_ssh_converter
from functions.vrf.ios.api.converter import _ios_vrf_api_converter
from functions.vrf.ios.netconf.converter import _ios_vrf_netconf_converter
from functions.vrf.ios.ssh.converter import _ios_vrf_ssh_converter
from functions.vrf.iosxr.ssh.converter import _iosxr_vrf_ssh_converter
from functions.vrf.iosxr.netconf.converter import _iosxr_vrf_netconf_converter
from functions.vrf.juniper.api.converter import _juniper_vrf_api_converter
from functions.vrf.juniper.netconf.converter import _juniper_vrf_netconf_converter
from functions.vrf.juniper.ssh.converter import _juniper_vrf_ssh_converter
from functions.vrf.napalm.converter import _napalm_vrf_converter
from functions.vrf.nxos.ssh.converter import _nxos_vrf_ssh_converter
from functions.vrf.nxos.netconf.converter import _nxos_vrf_netconf_converter
from functions.vrf.nxos.api.converter import _nxos_vrf_api_converter
from protocols.vrf import (
    VRF,
    ListVRF
)
from functions.global_tools import (
    open_file,
    open_txt_file,
    open_json_file,
    open_txt_file_as_bytes,
    printline
)
from behave import given, when, then


@given(u'A network protocols named VRF defined in protocols/vrf.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a VRF object equals to Arista manually named o0001')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a Arista API output named o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a Arista SSH output named o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object equals to Arista no config manually named o0011')
def step_impl(context):
    context.o0011 = ListVRF(
        vrf_lst=list()
    )

    context.o0011.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a Arista no config API output named o0012')
def step_impl(context):
    context.o0012 = _arista_vrf_api_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/api/"
                "arista_api_get_vrf_no_config.json"
            )
        )
    )


@given(u'I create a VRF object from a Arista no config Netconf named o0013')
def step_impl(context):
    context.o0013 = _arista_vrf_netconf_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/netconf/"
                "arista_nc_get_vrf_no_config.json"
            )
        )
    )


@given(u'I create a VRF object from a Arista no config SSH output named o0014')
def step_impl(context):
    context.o0014 = _arista_vrf_ssh_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/ssh/"
                "arista_cli_get_vrf_no_config.json"
            )
        )
    )


@given(u'I create a VRF object equals to Arista one vrf manually named o0021')
def step_impl(context):
    context.o0021 = ListVRF(
        vrf_lst=list()
    )

    context.o0021.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0021.vrf_lst.append(
        VRF(
            vrf_name="CUSTOMER_NETESTS",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a Arista one vrf API output named o0022')
def step_impl(context):
    context.o0022 = _arista_vrf_api_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/api/"
                "arista_api_get_vrf_one_vrf.json"
            )
        )
    )


@given(u'I create a VRF object from a Arista one vrf Netconf named o0023')
def step_impl(context):
    context.o0023 = _arista_vrf_netconf_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/netconf/"
                "arista_nc_get_vrf_one_vrf.json"
            )
        )
    )


@given(u'I create a VRF object from a Arista one vrf SSH output named o0024')
def step_impl(context):
    context.o0024 = _arista_vrf_ssh_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/arista/ssh/"
                "arista_cli_get_vrf_one_vrf.json"
            )
        )
    )


@given(u'I create a VRF object equals to Cumulus manually named o0101')
def step_impl(context):
    context.o0101 = ListVRF(
        vrf_lst=list()
    )

    context.o0101.vrf_lst.append(
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


@given(u'I create a VRF object from a Cumulus API output named o0102')
def step_impl(context):
    context.o0102 = _cumulus_vrf_api_converter(
        hostname="leaf01",
        cmd_output=open_txt_file_as_bytes(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/cumulus/api/"
                "cumulus_http_show_vrf.txt"
            )
        )
    )


@given(u'I create a VRF object from a Cumulus Netconf named o0103')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'I create a VRF object from a Cumulus SSH output named o0104')
def step_impl(context):
    context.o0104 = _cumulus_vrf_ssh_converter(
        hostname="leaf01",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/cumulus/ssh/"
                "cumulus_net_show_vrf.txt"
            )
        )
    )


@given(u'I create a VRF object equals to Extreme VSP manually named o0201')
def step_impl(context):
    context.o0201 = ListVRF(
        vrf_lst=list()
    )

    context.o0201.vrf_lst.append(
        VRF(
            vrf_name="GlobalRouter",
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

    context.o0201.vrf_lst.append(
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

    context.o0201.vrf_lst.append(
        VRF(
            vrf_name="MgmtRouter",
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


@given(u'I create a VRF object from a Extreme VSP API output named o0204')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'I create a VRF object from a Extreme VSP Netconf output named o0204')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'I create a VRF object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    context.o0204 = _extreme_vsp_vrf_ssh_converter(
        hostname="spine02",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/extreme_vsp/ssh/"
                "extreme_vsp_show_ip_vrf.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS manually named o0301')
def step_impl(context):
    context.o0301 = ListVRF(
        vrf_lst=list()
    )

    context.o0301.vrf_lst.append(
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

    context.o0301.vrf_lst.append(
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

    context.o0301.vrf_lst.append(
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


@given(u'I create a VRF object from a IOS API output named o0302')
def step_impl(context):
    context.o0302 = _ios_vrf_api_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/api/"
                "cisco_ios_api_get_vrf.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS Netconf named o0303')
def step_impl(context):
    context.o0303 = _ios_vrf_netconf_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/netconf/"
                "cisco_ios_nc_get_vrf.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS SSH named o0304')
def step_impl(context):
    context.o0304 = _ios_vrf_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/ssh/"
                "cisco_ios_show_ip_vrf_detail.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS no config manually named o0311')
def step_impl(context):
    context.o0311 = ListVRF(
        vrf_lst=list()
    )

    context.o0311.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS no config API named o0312')
def step_impl(context):
    context.o0312 = _ios_vrf_api_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/api/"
                "cisco_ios_api_get_vrf_no_config.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS no config Netconf named o0313')
def step_impl(context):
    context.o0313 = _ios_vrf_netconf_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/netconf/"
                "cisco_ios_nc_get_vrf_no_config.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS no config SSH named o0314')
def step_impl(context):
    context.o0314 = _ios_vrf_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/ssh/"
                "cisco_ios_ssh_get_vrf_no_config.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS one vrf manually named o0321')
def step_impl(context):
    context.o0321 = ListVRF(
        vrf_lst=list()
    )

    context.o0321.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0321.vrf_lst.append(
        VRF(
            vrf_name='CUSTOMER_001',
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd='65123:123',
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS one vrf API named o0322')
def step_impl(context):
    context.o0322 = _ios_vrf_api_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/api/"
                "cisco_ios_api_get_vrf_only_one.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS one vrf Netconf named o0323')
def step_impl(context):
    context.o0323 = _ios_vrf_netconf_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/netconf/"
                "cisco_ios_nc_get_vrf_only_one.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS one vrf SSH named o0324')
def step_impl(context):
    context.o0324 = _ios_vrf_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/ssh/"
                "cisco_ios_ssh_get_vrf_only_one.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS many manually named o0331')
def step_impl(context):
    context.o0331 = ListVRF(
        vrf_lst=list()
    )

    context.o0331.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0331.vrf_lst.append(
        VRF(
            vrf_name='CUSTOMER_001',
            vrf_id='1',
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd='65123:123',
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )
    
    context.o0331.vrf_lst.append(
        VRF(
            vrf_name='CUSTOMER_002',
            vrf_id='2',
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd='65123:123',
            rt_imp='65222:2',
            rt_exp='65222:1',
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS many API named o0332')
def step_impl(context):
    context.o0332 = _ios_vrf_api_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/api/"
                "cisco_ios_api_get_vrf_many.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS many Netconf named o0333')
def step_impl(context):
    context.o0333 = _ios_vrf_netconf_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/netconf/"
                "cisco_ios_nc_get_vrf_many.xml"
            )
        )
    )


@given(u'I create a VRF object from a IOS many SSH named o0334')
def step_impl(context):
    context.o0334 = _ios_vrf_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/ios/ssh/"
                "cisco_ios_ssh_get_vrf_many.txt"
            )
        )
    )



@given(u'I create a VRF object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.o0401 = ListVRF(
        vrf_lst=list()
    )

    context.o0401.vrf_lst.append(
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

    context.o0401.vrf_lst.append(
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


@given(u'I create a VRF object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a IOS-XR Netconf output named o403')
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

    context.o403 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.o0404 = _iosxr_vrf_ssh_converter(
        hostname="spine03",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/ssh/"
                "cisco_iosxr_show_vrf_all_detail.txt"
            )
        )
    )


@given(u'I create a VRF object equals IOS-XR multi manually output named o0405')
def step_impl(context):
    context.o0405 = ListVRF(
        vrf_lst=list()
    )

    context.o0405.vrf_lst.append(
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

    context.o0405.vrf_lst.append(
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

    context.o0405.vrf_lst.append(
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



@given(u'I create a VRF object from a IOS-XR multi Netconf output named o0406')
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

    context.o0406 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object equals to IOS-XR no config manually named o0411')
def step_impl(context):
    context.o0411 = ListVRF(
        vrf_lst=list()
    )


@given(u'I create a VRF object from a IOS-XR no config API named o0412')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a IOS-XR no config Netconf named o0413')
def step_impl(context):
    config = dict()
    config['VRF'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_vrf_no_config.xml"
        )
    )
    config['BGP'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_bgp_no_config.xml"
        )
    )

    context.o0413 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object from a IOS-XR no config SSH named o0414')
def step_impl(context):
    context.o0414 = _iosxr_vrf_ssh_converter(
        hostname="spine03",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/ssh/"
                "cisco_iosxr_show_vrf_all_detail_no_config.txt"
            )
        )
    )


@given(u'I create a VRF object equals to IOS-XR one vrf manually named o0421')
def step_impl(context):
    context.o0421 = ListVRF(
        vrf_lst=list()
    )

    context.o0421.vrf_lst.append(
        VRF(
            vrf_name="CUSTOMER_NETESTS",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a IOS-XR one vrf API named o0422')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VRF object from a IOS-XR one vrf Netconf named o0423')
def step_impl(context):
    config = dict()
    config['VRF'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_vrf_one_vrf.xml"
        )
    )
    config['BGP'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/netconf/"
            "cisco_iosxr_nc_get_bgp_one_vrf.xml"
        )
    )

    context.o0423 = _iosxr_vrf_netconf_converter(
        hostname="spine03",
        cmd_output=config
    )


@given(u'I create a VRF object from a IOS-XR one vrf SSH named o0424')
def step_impl(context):
    context.o0424 = _iosxr_vrf_ssh_converter(
        hostname="spine03",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/iosxr/ssh/"
                "cisco_iosxr_show_vrf_all_detail_one_vrf.txt"
            )
        )
    )



@given(u'I create a VRF object equals to Juniper manually named o0501')
def step_impl(context):
    context.o0501 = ListVRF(
        vrf_lst=list()
    )

    context.o0501.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id="100.123.1.0",
            vrf_type="forwarding",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0501.vrf_lst.append(
        VRF(
            vrf_name="CUSTOMER_001",
            vrf_id="7.7.7.7",
            vrf_type="vrf",
            l3_vni=NOT_SET,
            rd="65333:333",
            rt_imp="__vrf-import-CUSTOMER_001-internal__",
            rt_exp="__vrf-export-CUSTOMER_001-internal__",
            imp_targ="65333:333",
            exp_targ="65333:333"
        )
    )

    context.o0501.vrf_lst.append(
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


@given(u'I create a VRF object from a Juniper API output named o0502')
def step_impl(context):
    context.o0502 = _juniper_vrf_api_converter(
        hostname="leaf04",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/juniper/api/"
                "juniper_api_get_vrf.xml"
            )
        )
    )


@given(u'I create a VRF object from a Juniper Netconf output named o0503')
def step_impl(context):
    context.o0503 = _juniper_vrf_netconf_converter(
        hostname="leaf04",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/juniper/netconf/"
                "get_instance_information_details.xml"
            )
        )
    )


@given(u'I create a VRF object from a Juniper SSH output named o0504')
def step_impl(context):
    context.o0504 = _juniper_vrf_ssh_converter(
        hostname="leaf04",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/juniper/ssh/"
                "juniper_show_route_instance_detail.json"
            )
        )
    )


@given(u'I create a VRF object equals to NAPALM manually named o0601')
def step_impl(context):
    context.o0601 = ListVRF(
        vrf_lst=list()
    )

    context.o0601.vrf_lst.append(
        VRF(
            vrf_name="MGMT_VRF",
            vrf_id=NOT_SET,
            vrf_type="L3VRF",
            l3_vni=NOT_SET,
            rd="65000:999",
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0601.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type="DEFAULT_INSTANCE",
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )


@given(u'I create a VRF object from a NAPALM output named o0602')
def step_impl(context):
    context.o0602 = _napalm_vrf_converter(
        hostname="leaf02",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/napalm/napalm_get_vrf.json"
            )
        )
    )


@given(u'I create a VRF object equals to NXOS manually named o0701')
def step_impl(context):
    context.o0701 = ListVRF(
        vrf_lst=list()
    )

    context.o0701.vrf_lst.append(
        VRF(
            vrf_name="CUSTOMER_001",
            vrf_id="4",
            vrf_type=NOT_SET,
            l3_vni="1000",
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0701.vrf_lst.append(
        VRF(
            vrf_name="INTERNAL_PEERING",
            vrf_id="3",
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd='65432:222',
            rt_imp='65432:22',
            rt_exp='65432:22',
            imp_targ=NOT_SET,
            exp_targ=NOT_SET
        )
    )

    context.o0701.vrf_lst.append(
        VRF(
            vrf_name="management",
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

    context.o0701.vrf_lst.append(
        VRF(
            vrf_name="default",
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


@given(u'I create a VRF object from a NXOS API output named o0702')
def step_impl(context):
    context.o0702 = _nxos_vrf_api_converter(
        hostname="leaf02",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/nxos/api/"
                "cisco_nxos_api_get_vrf.xml"
            )
        )
    )


@given(u'I create a VRF object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.o0703 = _nxos_vrf_netconf_converter(
        hostname="leaf02",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/nxos/netconf/"
                "cisco_nxos_nc_get_vrf.xml"
            )
        )
    )


@given(u'I create a VRF object from a NXOS SSH output named o0704')
def step_impl(context):
    context.o0704 = _nxos_vrf_ssh_converter(
        hostname="leaf02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vrf/nxos/ssh/"
                "cisco_nxos_show_vrf_all_detail.json"
            )
        )
    )


@given(u'VRF o0001 should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0001 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0002 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0011 should be equal to o0012')
def step_impl(context):
    assert context.o0011 == context.o0012

@given(u'VRF o0011 should be equal to o0013')
def step_impl(context):
    assert context.o0011 == context.o0013


@given(u'VRF o0011 should be equal to o0014')
def step_impl(context):
    assert context.o0011 == context.o0014


@given(u'VRF o0012 should be equal to o0013')
def step_impl(context):
    assert context.o0012 == context.o0013


@given(u'VRF o0012 should be equal to o0014')
def step_impl(context):
    assert context.o0012 == context.o0014


@given(u'VRF o0013 should be equal to o0014')
def step_impl(context):
    assert context.o0013 == context.o0014


@given(u'VRF o0021 should be equal to o0022')
def step_impl(context):
    assert context.o0021 == context.o0022


@given(u'VRF o0021 should be equal to o0023')
def step_impl(context):
    assert context.o0021 == context.o0023


@given(u'VRF o0021 should be equal to o0024')
def step_impl(context):
    assert context.o0021 == context.o0024


@given(u'VRF o0022 should be equal to o0023')
def step_impl(context):
    assert context.o0022 == context.o0023


@given(u'VRF o0022 should be equal to o0024')
def step_impl(context):
    assert context.o0022 == context.o0024


@given(u'VRF o0023 should be equal to o0024')
def step_impl(context):
    assert context.o0023 == context.o0024


@given(u'VRF o0101 should be equal to o0102')
def step_impl(context):
    assert context.o0101 == context.o0102


@given(u'VRF o0101 should be equal to o0103')
def step_impl(context):
    print("Cumulus VRF with Netconf not possible -> Not tested")


@given(u'VRF o0101 should be equal to o0104')
def step_impl(context):
    assert context.o0101 == context.o0104


@given(u'VRF o0102 should be equal to o0103')
def step_impl(context):
    print("Cumulus VRF with Netconf not possible -> Not tested")


@given(u'VRF o0102 should be equal to o0104')
def step_impl(context):
    assert context.o0102 == context.o0104


@given(u'VRF o0103 should be equal to o0104')
def step_impl(context):
    print("Cumulus VRF with Netconf not possible -> Not tested")


@given(u'VRF YAML file should be equal to o0102')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o0102,
        test=True
    )


@given(u'VRF YAML file should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0104')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf01",
        groups=['linux'],
        vrf_host_data=context.o0104,
        test=True
    )


@given(u'VRF o0201 should be equal to o0202')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'VRF o0201 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'VRF o0201 should be equal to o0204')
def step_impl(context):
    assert context.o0201 == context.o0204


@given(u'VRF o0202 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'VRF o0202 should be equal to o0204')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'VRF o0203 should be equal to o0204')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'VRF YAML file should be equal to o0202')
def step_impl(context):
    print("Extreme VSP VRF with API has no endpoint -> Not tested")


@given(u'VRF YAML file should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'VRF YAML file should be equal to o0204')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine02",
        groups=['extreme_vsp'],
        vrf_host_data=context.o0204,
        test=True
    )


@given(u'VRF o0301 should be equal to o0302')
def step_impl(context):
    assert context.o0301 == context.o0302


@given(u'VRF o0301 should be equal to o0303')
def step_impl(context):
    assert context.o0301 == context.o0303


@given(u'VRF o0301 should be equal to o0304')
def step_impl(context):
    assert context.o0301 == context.o0304


@given(u'VRF o0302 should be equal to o0303')
def step_impl(context):
    assert context.o0302 == context.o0303


@given(u'VRF o0302 should be equal to o0304')
def step_impl(context):
    assert context.o0302 == context.o0304


@given(u'VRF o0303 should be equal to o0304')
def step_impl(context):
    assert context.o0303 == context.o0304


@given(u'VRF o0311 should be equal to o0312')
def step_impl(context):
    assert context.o0311 == context.o0312


@given(u'VRF o0311 should be equal to o0313')
def step_impl(context):
    assert context.o0311 == context.o0313


@given(u'VRF o0311 should be equal to o0314')
def step_impl(context):
    assert context.o0311 == context.o0314


@given(u'VRF o0312 should be equal to o0313')
def step_impl(context):
    assert context.o0312 == context.o0313


@given(u'VRF o0312 should be equal to o0314')
def step_impl(context):
    assert context.o0312 == context.o0314


@given(u'VRF o0313 should be equal to o0314')
def step_impl(context):
    assert context.o0313 == context.o0314


@given(u'VRF o0321 should be equal to o0322')
def step_impl(context):
    assert context.o0321 == context.o0322


@given(u'VRF o0321 should be equal to o0323')
def step_impl(context):
    assert context.o0321 == context.o0323


@given(u'VRF o0321 should be equal to o0324')
def step_impl(context):
    assert context.o0321 == context.o0324


@given(u'VRF o0322 should be equal to o0323')
def step_impl(context):
    assert context.o0322 == context.o0323


@given(u'VRF o0322 should be equal to o0324')
def step_impl(context):
    assert context.o0322== context.o0324


@given(u'VRF o0323 should be equal to o0324')
def step_impl(context):
    assert context.o0323 == context.o0324


@given(u'VRF o0331 should be equal to o0332')
def step_impl(context):
    assert context.o0331 == context.o0332


@given(u'VRF o0331 should be equal to o0333')
def step_impl(context):
    assert context.o0331 == context.o0333


@given(u'VRF o0331 should be equal to o0334')
def step_impl(context):
    assert context.o0331 == context.o0334


@given(u'VRF o0332 should be equal to o0333')
def step_impl(context):
    assert context.o0332 == context.o0333


@given(u'VRF o0332 should be equal to o0334')
def step_impl(context):
    assert context.o0332 == context.o0334


@given(u'VRF o0333 should be equal to o0334')
def step_impl(context):
    assert context.o0333 == context.o0334


@given(u'VRF YAML file should be equal to o0302')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf05",
        groups=['ios'],
        vrf_host_data=context.o0302,
        test=True
    )


@given(u'VRF YAML file should be equal to o0303')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf05",
        groups=['ios'],
        vrf_host_data=context.o0303,
        test=True
    )


@given(u'VRF YAML file should be equal to o0304')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf05",
        groups=['ios'],
        vrf_host_data=context.o0304,
        test=True
    )


@given(u'VRF o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0401 should be equal to o0404')
def step_impl(context):
    assert context.o0401 == context.o0404


@given(u'VRF o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0405 should be equal to o0406')
def step_impl(context):
    assert context.o0405 == context.o0406

@given(u'VRF YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF YAML file should be equal to o0404')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="spine03",
        groups=['iosxr'],
        vrf_host_data=context.o0404,
        test=True
    )


@given(u'VRF o0411 should be equal to o0412')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0411 should be equal to o0413')
def step_impl(context):
    assert context.o0411 == context.o0413


@given(u'VRF o0411 should be equal to o0414')
def step_impl(context):
    assert context.o0411 == context.o0414


@given(u'VRF o0412 should be equal to o0413')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0412 should be equal to o0414')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0413 should be equal to o0414')
def step_impl(context):
    assert context.o0413 == context.o0414


@given(u'VRF o0421 should be equal to o0422')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0421 should be equal to o0423')
def step_impl(context):
    assert context.o0421 == context.o0423


@given(u'VRF o0421 should be equal to o0424')
def step_impl(context):
    assert context.o0421 == context.o0424


@given(u'VRF o0422 should be equal to o0423')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0422 should be equal to o0424')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VRF o0423 should be equal to o0424')
def step_impl(context):
    assert context.o0423 == context.o0424


@given(u'VRF o0501 should be equal to o0502')
def step_impl(context):
    assert context.o0501 == context.o0502


@given(u'VRF o0501 should be equal to o0503')
def step_impl(context):
    assert context.o0501 == context.o0503


@given(u'VRF o0501 should be equal to o0504')
def step_impl(context):
    assert context.o0501 == context.o0504


@given(u'VRF o0502 should be equal to o0503')
def step_impl(context):
    assert context.o0502 == context.o0503


@given(u'VRF o0502 should be equal to o0504')
def step_impl(context):
    assert context.o0502 == context.o0504


@given(u'VRF o0503 should be equal to o0504')
def step_impl(context):
    assert context.o0503 == context.o0504


@given(u'VRF YAML file should be equal to o0502')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o0502,
        test=True
    )


@given(u'VRF YAML file should be equal to o0503')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o0503,
        test=True
    )


@given(u'VRF YAML file should be equal to o0504')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf04",
        groups=['junos'],
        vrf_host_data=context.o0504,
        test=True
    )


@given(u'VRF o0601 should be equal to o0602')
def step_impl(context):
    assert context.o0601 == context.o0602


@given(u'VRF o0701 should be equal to o0702')
def step_impl(context):
    assert context.o0701 == context.o0702


@given(u'VRF o0701 should be equal to o0703')
def step_impl(context):
    assert context.o0701 == context.o0703


@given(u'VRF o0701 should be equal to o0704')
def step_impl(context):
    assert context.o0701 == context.o0704


@given(u'VRF o0702 should be equal to o0703')
def step_impl(context):
    assert context.o0702 == context.o0703


@given(u'VRF o0702 should be equal to o0704')
def step_impl(context):
    assert context.o0702 == context.o0704


@given(u'VRF o0703 should be equal to o0704')
def step_impl(context):
    assert context.o0703 == context.o0704


@given(u'VRF YAML file should be equal to o0702')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf02",
        groups=['nxos'],
        vrf_host_data=context.o0702,
        test=True
    )


@given(u'VRF YAML file should be equal to o0703')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf02",
        groups=['nxos'],
        vrf_host_data=context.o0703,
        test=True
    )


@given(u'VRF YAML file should be equal to o0704')
def step_impl(context):
    assert _compare_vrf(
        host_keys=VRF_DATA_KEY,
        hostname="leaf02",
        groups=['nxos'],
        vrf_host_data=context.o0704,
        test=True
    )


@given(u'I Finish my VRF tests and list tests not implemented')
def step_impl(context):
    printline()
    print("| The following tests are not implemented :")
    printline()
    for test in context.test_not_implemented:
        print(f"| {test}")
    printline()
