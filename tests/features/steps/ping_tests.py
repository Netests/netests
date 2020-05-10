#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.global_tools import open_txt_file, open_json_file
from functions.ping.arista.api.ping import arista_api_validate_output
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
from exceptions.netests_exceptions import NetestsErrorWithPingExecution
from const.constants import (
    FEATURES_SRC_PATH,
    ARISTA_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME,
    API_CONNECTION,
    NETCONF_CONNECTION,
    SSH_CONNECTION
)


@given(u'A network protocols named PING defined in protocols/ping.py')
def step_impl(context):
    context.test_not_implemented = list()

@given(u'A Ping output from a Arista CLI that works named o0001')
def step_impl(context):
    context.o0001 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/ssh/"
            "arista_ping_works.txt"
        )
    )


@given(u'A Ping output from a Arista CLI with wrong VRF named o0002')
def step_impl(context):
    context.o0002 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/ssh/"
            "arista_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Arista CLI with wrong IPv4 named o0003')
def step_impl(context):
    context.o0003 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/ssh/"
            "arista_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Arista CLI with unreachable IPv4 named o0004')
def step_impl(context):
    context.o0004 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/ssh/"
            "arista_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Arista CLI with no route to IPv4 named o0005')
def step_impl(context):
    context.o0005 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/ssh/"
            "arista_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Arista API that works named o0011')
def step_impl(context):
    context.o0011 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/api/"
            "arista_ping_works.json"
        )
    )


@given(u'A Ping output from a Arista API with wrong VRF named o0012')
def step_impl(context):
    context.o0012 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/api/"
            "arista_ping_wrong_vrf.json"
        )
    )


@given(u'A Ping output from a Arista API with wrong IPv4 named o0013')
def step_impl(context):
    context.o0013 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/api/"
            "arista_ping_wrong_ip.json"
        )
    )


@given(u'A Ping output from a Arista API with unreachable IPv4 named o0014')
def step_impl(context):
    context.o0014 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/api/"
            "arista_ping_unreachable.json"
        )
    )


@given(u'A Ping output from a Arista API with no route to IPv4 named o0015')
def step_impl(context):
    context.o0015 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/arista/api/"
            "arista_ping_no_route.json"
        )
    )


@given(u'A Ping output from a Cumulus CLI that works named o0101')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'A Ping output from a Cumulus CLI with wrong VRF named o0102')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'A Ping output from a Cumulus CLI with wrong IPv4 named o0103')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'A Ping output from a Cumulus CLI with unreachable IPv4 named o0104')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'A Ping output from a Cumulus CLI with no route to IPv4 named o0105')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'A Ping output from a Extreme VSP CLI that works named o0201')
def step_impl(context):
    context.o0201 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/extreme_vsp/ssh/"
            "extreme_vsp_ping_works.txt"
        )
    )


@given(u'A Ping output from a Extreme VSP CLI with wrong VRF named o0202')
def step_impl(context):
    context.o0202 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/extreme_vsp/ssh/"
            "extreme_vsp_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Extreme VSP CLI with wrong IPv4 named o0203')
def step_impl(context):
    context.o0203 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/extreme_vsp/ssh/"
            "extreme_vsp_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Extreme VSP CLI with unreachable IPv4 named o0204')
def step_impl(context):
    context.o0204 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/extreme_vsp/ssh/"
            "extreme_vsp_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Extreme VSP CLI with no route to IPv4 named o0205')
def step_impl(context):
    context.o0205 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/extreme_vsp/ssh/"
            "extreme_vsp_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI that works named o0301')
def step_impl(context):
    context.o0301 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_works.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with wrong VRF named o0302')
def step_impl(context):
    context.o0302 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with wrong IPv4 named o0303')
def step_impl(context):
    context.o0303 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with unreachable IPv4 named o0304')
def step_impl(context):
    context.o0304 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with no route to IPv4 named o0305')
def step_impl(context):
    context.o0305 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with no src ip to IPv4 named o0306')
def step_impl(context):
    context.o0306 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_vrf_no_ip_src.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XE CLI with no vrf config to IPv4 named o0307')
def step_impl(context):
    context.o0307 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/ios/ssh/"
            "ios_ping_no_vrf_configured.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR CLI that works named o0401')
def step_impl(context):
    context.o0401 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/ssh/"
            "iosxr_ping_works.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR CLI with wrong VRF named o0402')
def step_impl(context):
    context.o0402 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/ssh/"
            "iosxr_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR CLI with wrong IPv4 named o0403')
def step_impl(context):
    context.o0403 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/ssh/"
            "iosxr_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR CLI with unreachable IPv4 named o0404')
def step_impl(context):
    context.o0404 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/ssh/"
            "iosxr_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR CLI with no route to IPv4 named o0405')
def step_impl(context):
    context.o0405 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/ssh/"
            "iosxr_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR Netconf that works named o0411')
def step_impl(context):
    context.o0411 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/netconf/"
            "iosxr_ping_works.json"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR Netconf with wrong VRF named o0412')
def step_impl(context):
    context.o0412 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/netconf/"
            "iosxr_ping_wrong_vrf.json"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR Netconf with wrong IPv4 named o0413')
def step_impl(context):
    context.o0413 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/netconf/"
            "iosxr_ping_wrong_ip.json"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR Netconf with unreachable IPv4 named o0414')
def step_impl(context):
    context.o0414 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/netconf/"
            "iosxr_ping_unreachable.json"
        )
    )


@given(u'A Ping output from a Cisco IOS-XR Netconf with no route to IPv4 named o0415')
def step_impl(context):
    context.o0415 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/iosxr/netconf/"
            "iosxr_ping_no_route.json"
        )
    )


@given(u'A Ping output from a Cisco NXOS CLI that works named o0501')
def step_impl(context):
    context.o0501 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/ssh/"
            "nxos_ping_works.txt"
        )
    )


@given(u'A Ping output from a Cisco NXOS CLI with wrong VRF named o0502')
def step_impl(context):
    context.o0502 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/ssh/"
            "nxos_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Cisco NXOS CLI with wrong IPv4 named o0503')
def step_impl(context):
    context.o0503 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/ssh/"
            "nxos_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Cisco NXOS CLI with unreachable IPv4 named o0504')
def step_impl(context):
    context.o0504 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/ssh/"
            "nxos_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Cisco NXOS CLI with no route to IPv4 named o0505')
def step_impl(context):
    context.o0505 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/ssh/"
            "nxos_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Cisco NXOS Netconf that works named o0511')
def step_impl(context):
    context.o0511 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/api/"
            "nxos_ping_works.json"
        )
    )


@given(u'A Ping output from a Cisco NXOS Netconf with wrong VRF named o0512')
def step_impl(context):
    context.o0512 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/api/"
            "nxos_ping_wrong_vrf.json"
        )
    )


@given(u'A Ping output from a Cisco NXOS Netconf with wrong IPv4 named o0513')
def step_impl(context):
    context.o0513 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/api/"
            "nxos_ping_wrong_ip.json"
        )
    )


@given(u'A Ping output from a Cisco NXOS Netconf with unreachable IPv4 named o0514')
def step_impl(context):
    context.o0514 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/api/"
            "nxos_ping_unreachable.json"
        )
    )


@given(u'A Ping output from a Cisco NXOS Netconf with no route to IPv4 named o0515')
def step_impl(context):
    context.o0515 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/nxos/api/"
            "nxos_ping_no_route.json"
        )
    )


@given(u'A Ping output from a Juniper CLI that works named o0601')
def step_impl(context):
    context.o0601 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_works.txt"
        )
    )


@given(u'A Ping output from a Juniper CLI with wrong VRF named o0602')
def step_impl(context):
    context.o0602 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_wrong_vrf.txt"
        )
    )


@given(u'A Ping output from a Juniper CLI with wrong IPv4 named o0603')
def step_impl(context):
    context.o0603 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_wrong_ip.txt"
        )
    )


@given(u'A Ping output from a Juniper CLI with unreachable IPv4 named o0604')
def step_impl(context):
    context.o0604 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_unreachable.txt"
        )
    )


@given(u'A Ping output from a Juniper CLI with no route to IPv4 named o0605')
def step_impl(context):
    context.o0605 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_no_route.txt"
        )
    )


@given(u'A Ping output from a Juniper CLI with no src ip to IPv4 named o0606')
def step_impl(context):
    context.o0606 = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/ssh/"
            "juniper_ping_no_src_ip.txt"
        )
    )


@given(u'A Ping output from a Juniper Netconf that works named o0611')
def step_impl(context):
    context.o0611 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_works.json"
        )
    )


@given(u'A Ping output from a Juniper Netconf with wrong VRF named o0612')
def step_impl(context):
    context.o0612 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_wrong_vrf.json"
        )
    )


@given(u'A Ping output from a Juniper Netconf with wrong IPv4 named o0613')
def step_impl(context):
    context.o0613 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_wrong_ip.json"
        )
    )


@given(u'A Ping output from a Juniper Netconf with unreachable IPv4 named o0614')
def step_impl(context):
    context.o0614 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_unreachable.json"
        )
    )


@given(u'A Ping output from a Juniper Netconf with no route to IPv4 named o0615')
def step_impl(context):
    context.o0615 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_no_route.json"
        )
    )


@given(u'A Ping output from a Juniper Netconf with no src ip to IPv4 named o0616')
def step_impl(context):
    context.o0616 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/netconf/"
            "juniper_ping_no_src_ip.json"
        )
    )


@given(u'A Ping output from a Juniper API that works named o0621')
def step_impl(context):
    context.o0621 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_works.json"
        )
    )


@given(u'A Ping output from a Juniper API with wrong VRF named o0622')
def step_impl(context):
    context.o0622 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_wrong_vrf.json"
        )
    )


@given(u'A Ping output from a Juniper API with wrong IPv4 named o0623')
def step_impl(context):
    context.o0623 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_wrong_ip.json"
        )
    )


@given(u'A Ping output from a Juniper API with unreachable IPv4 named o0624')
def step_impl(context):
    context.o0624 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_unreachable.json"
        )
    )



@given(u'A Ping output from a Juniper API with no route to IPv4 named o0625')
def step_impl(context):
    context.o0625 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_no_route.json"
        )
    )


@given(u'A Ping output from a Juniper API with no src ip to IPv4 named o0626')
def step_impl(context):
    context.o0626 = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ping/juniper/api/"
            "juniper_ping_no_src_ip.json"
        )
    )



@given(u'Ping Arista CLI works does named o0001 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0001,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0001",
            must_work=True
        )
    except Exception:
        assert False


@given(u'Ping Arista CLI wrong VRF named o0002 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0002,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0002",
            must_work=False
        )
    except Exception:
        assert False


@given(u'Ping Arista CLI wrong IPv4 named o0003 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0003,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0002",
            must_work=False
        )
    except Exception:
        assert False


@given(u'Ping Arista CLI unreachable named o0004 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0004,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0002",
            must_work=False
        )
    except Exception:
        assert False


@given(u'Ping Arista CLI no route named o0005 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0005,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0002",
            must_work=False
        )
    except Exception:
        assert False


@given(u'Ping Arista CLI works does named o0001 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0001,
            hostname='spine03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0001",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista CLI wrong VRF named o0002 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0002,
            hostname='spine03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0002",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista CLI wrong IPv4 named o0003 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0003,
            hostname='spine03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0003",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista CLI unreachable named o0004 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0004,
            hostname='spine03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0004",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista CLI no route named o0005 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0005,
            hostname='spine03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0005",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True



@given(u'Ping Arista API works does named o0011 not raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0011,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0011",
            ping_works=True
        )
    except Exception:
        assert False


@given(u'Ping Arista API wrong VRF named o0012 raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0012,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0012",
            ping_works=False
        )
    except Exception:
        assert False


@given(u'Ping Arista API wrong IPv4 named o0013 raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0013,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0013",
            ping_works=False
        )
    except Exception:
        assert False


@given(u'Ping Arista API unreachable named o0014 raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0014,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0014",
            ping_works=False
        )
    except Exception:
        assert False


@given(u'Ping Arista API no route named o0015 raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0015,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0015",
            ping_works=False
        )
    except Exception:
        assert False


@given(u'Ping Arista API works does named o0011 not raise an Exception reverse')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0011,
            hostname='leaf03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0011",
            ping_works=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista API wrong VRF named o0012 raise an Exception reverse')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0012,
            hostname='leaf03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0012",
            ping_works=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista API wrong IPv4 named o0013 raise an Exception reverse')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0013,
            hostname='leaf03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0013",
            ping_works=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista API unreachable named o0014 raise an Exception reverse')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0014,
            hostname='leaf03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0014",
            ping_works=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Arista API no route named o0015 raise an Exception reverse')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0015,
            hostname='leaf03',
            platform=ARISTA_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_print="o0015",
            ping_works=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cumulus CLI works does named o0101 not raise an Exception')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'Ping Cumulus CLI wrong VRF named o0102 raise an Exception')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'Ping Cumulus CLI wrong IPv4 named o0103 raise an Exception')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'Ping Cumulus CLI unreachable named o0104 raise an Exception')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'Ping Cumulus CLI no route named o0105 raise an Exception')
def step_impl(context):
    print("Cumulus - Ping execute with 'remote_command' => Not tested")


@given(u'Ping Extreme VSP CLI works does named o0201 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0201,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0201",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Extreme VSP CLI wrong VRF named o0202 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0202,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0202",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Extreme VSP CLI wrong IPv4 named o0203 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0202,
            hostname='spine03',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0203",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Extreme VSP CLI unreachable named o0204 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0204,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0204",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Extreme VSP CLI no route named o0205 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0205,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0205",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Extreme VSP CLI works does named o0201 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0201,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0201",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Extreme VSP CLI wrong VRF named o0202 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0202,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0202",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Extreme VSP CLI wrong IPv4 named o0203 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0203,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0203",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Extreme VSP CLI unreachable named o0204 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0204,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0204",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Extreme VSP CLI no route named o0205 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0205,
            hostname='spine02',
            platform=EXTREME_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0205",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI works does named o0301 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0301,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0301",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI wrong VRF named o0302 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0302,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0302",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI wrong IPv4 named o0303 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0303,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0303",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI unreachable named o0304 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0304,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0304",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI no route named o0305 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0305,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0305",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI no src ip named o0306 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0306,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0306",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI no vrf config named o0307 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0307,
            hostname='leaf05',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0307",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XE CLI works does named o0301 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0301,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0301",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI wrong VRF named o0302 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0302,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0302",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI wrong IPv4 named o0303 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0303,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0303",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI unreachable named o0304 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0304,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0304",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI no route named o0305 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0305,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0305",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI no src ip named o0306 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0306,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0306",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XE CLI no vrf config named o0307 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0307,
            hostname='spine03',
            platform=CISCO_IOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0307",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR CLI works does named o0401 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0401,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0401",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR CLI wrong VRF named o0402 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0402,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0402",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR CLI wrong IPv4 named o0403 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0403,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0403",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR CLI unreachable named o0404 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0404,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0404",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR CLI no route named o0405 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0405,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0405",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR CLI works does named o0401 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0401,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0401",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR CLI wrong VRF named o0402 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0403,
            hostname='spine02',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0402",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR CLI wrong IPv4 named o0403 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0403,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0403",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR CLI unreachable named o0404 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0404,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0404",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR CLI no route named o0405 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0405,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0405",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True



@given(u'Ping Cisco IOS-XR Netconf works does named o0411 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0411,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0411",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR Netconf wrong VRF named o0412 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0412,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0412",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR Netconf wrong IPv4 named o0413 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0413,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0413",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR Netconf unreachable named o0414 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0414,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0414",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR Netconf no route named o0415 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0415,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0415",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco IOS-XR Netconf works does named o0411 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0411,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0411",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR Netconf wrong VRF named o0412 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0413,
            hostname='spine02',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0412",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR Netconf wrong IPv4 named o0413 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0413,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0413",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR Netconf unreachable named o0414 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0414,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0414",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco IOS-XR Netconf no route named o0415 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0415,
            hostname='spine03',
            platform=CISCO_IOSXR_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0415",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS CLI works does named o0501 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0501,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0501",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS CLI wrong VRF named o0502 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0502,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0502",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS CLI wrong IPv4 named o0503 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0503,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0503",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS CLI unreachable named o0504 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0504,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0504",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS CLI no route named o0505 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0505,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0505",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS CLI works does named o0501 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0501,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0501",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS CLI wrong VRF named o0502 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0502,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0502",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS CLI wrong IPv4 named o0503 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0503,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0503",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS CLI unreachable named o0504 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0504,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0504",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS CLI no route named o0505 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0505,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0505",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS Netconf works does named o0511 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0511,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0511",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS Netconf wrong VRF named o0512 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0512,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0512",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS Netconf wrong IPv4 named o0513 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0513,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0513",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS Netconf unreachable named o0514 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0514,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0514",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS Netconf no route named o0515 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0515,
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0515",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Cisco NXOS Netconf works does named o0511 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0511.get('result').get('msg'),
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0511",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS Netconf wrong VRF named o0512 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0512.get('result').get('msg'),
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0512",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS Netconf wrong IPv4 named o0513 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0513.get('result').get('msg'),
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0513",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS Netconf unreachable named o0514 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0514.get('result').get('msg'),
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0514",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Cisco NXOS Netconf no route named o0515 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0515.get('result').get('msg'),
            hostname='leaf02',
            platform=NEXUS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0515",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper CLI works does named o0601 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0601,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0601",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI wrong VRF named o0602 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0602,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0602",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI wrong IPv4 named o0603 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0603,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0603",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI unreachable named o0604 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0604,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0604",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI no route named o0605 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0605,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0605",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI no src ip named o0606 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0606,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0606",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper CLI works does named o0601 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0601,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0601",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True

@given(u'Ping Juniper CLI wrong VRF named o0602 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0602,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0602",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper CLI wrong IPv4 named o0603 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0603,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0603",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper CLI unreachable named o0604 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0604,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0604",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper CLI no route named o0605 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0605,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0605",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper CLI no src ip named o0606 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0606,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=SSH_CONNECTION,
            ping_line="o0606",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf works does named o0611 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0611,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0611",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf wrong VRF named o0612 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0612,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0612",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf wrong IPv4 named o0613 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0613,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0613",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf unreachable named o0614 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0614,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0614",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf no route named o0615 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0615,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0615",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf no src ip named o0616 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0616,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0616",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper Netconf works does named o0611 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0611,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0611",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf wrong VRF named o0612 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0612,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0612",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf wrong IPv4 named o0613 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0613,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0613",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf unreachable named o0614 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0614,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0614",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf no route named o0615 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0615,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0615",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper Netconf no src ip named o0616 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0616,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=NETCONF_CONNECTION,
            ping_line="o0616",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API works does named o0621 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0621,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0621",
            must_work=True
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API wrong VRF named o0622 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0622,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0622",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API wrong IPv4 named o0623 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0623,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0623",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API unreachable named o0624 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0624,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o064",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API no route named o0625 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0625,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0625",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API no src ip named o0626 raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0626,
            hostname='leaf02',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0626",
            must_work=False
        )
    except NetestsErrorWithPingExecution:
        assert False


@given(u'Ping Juniper API works does named o0621 not raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0621,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0621",
            must_work=False
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API wrong VRF named o0622 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0622,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0622",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API wrong IPv4 named o0623 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0623,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0623",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API unreachable named o0624 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0624,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0624",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API no route named o0625 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0625,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0625",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True


@given(u'Ping Juniper API no src ip named o0626 raise an Exception reverse')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0626,
            hostname='leaf04',
            platform=JUNOS_PLATEFORM_NAME,
            connexion=API_CONNECTION,
            ping_line="o0626",
            must_work=True
        )
        assert False
    except NetestsErrorWithPingExecution:
        assert True
