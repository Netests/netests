#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.global_tools import open_txt_file, open_json_file
from functions.ping.arista.api.ping import arista_api_validate_output
from functions.ping.ping_validator import _raise_exception_on_ping_cmd
from const.constants import (
    FEATURES_SRC_PATH,
    ARISTA_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME
)


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


@given(u'Ping Arista CLI works does named o0001 not raise an Exception')
def step_impl(context):
    try:
        _raise_exception_on_ping_cmd(
            output=context.o0001,
            hostname="leaf02",
            platform=ARISTA_PLATEFORM_NAME,
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
            ping_line="o0002",
            must_work=False
        )
    except Exception:
        assert False


@given(u'Ping Arista API works does named o0011 not raise an Exception')
def step_impl(context):
    try:
        arista_api_validate_output(
            output=context.o0011,
            hostname='leaf02',
            platform=ARISTA_PLATEFORM_NAME,
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
            ping_print="o0015",
            ping_works=False
        )
    except Exception:
        assert False
