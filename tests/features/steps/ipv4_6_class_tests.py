#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import ValidationError
from netests.constants import NOT_SET
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.ip import IPAddress


@given(u'I create a IPAddress object named o0000')
def step_impl(context):
    data = {
        "ip_address": "192.168.1.1",
        "netmask": "255.255.255.0",
        "options": {}
    }
    context.o0000 = IPAddress(**data)


@given(u'I create a IPV4 object named o0001')
def step_impl(context):
    context.o0001 = IPV4(
        ip_address="192.168.1.1",
        netmask="255.255.255.0",
        options={}
    )


@given(u'I create a wrong IPV4 object named o0002')
def step_impl(context):
    try:
        context.o0002 = IPV4(
            ip_address=NOT_SET,
            netmask=NOT_SET,
            options={}
        )
        assert False
    except ValidationError:
        assert True


@given(u'I create a IPV4Interface named o0003')
def step_impl(context):
    ipv4_lst = [
        IPV4(
            ip_address="192.168.1.1",
            netmask="255.255.255.0",
            options={}
        ),
        IPV4(
            ip_address="192.168.1.2",
            netmask="255.255.255.0",
            options={}
        )
    ]
    context.o0003 = IPV4Interface(
        ipv4_addresses=ipv4_lst
    )


@given(u'I create a wrong IPV4Interface named o0004')
def step_impl(context):
    try:
        ipv4_lst = [
            {
                "ip_address": "192.168.1.1",
                "netmask": "255.255.255.0",
                "options": {}
            },
            "Not an IP Object"
        ]
        context.o0004 = IPV4Interface(
            ipv4_addresses=ipv4_lst
        )
        assert False
    except ValidationError:
        assert True


@given(u'I create a IPAddress object named o0010')
def step_impl(context):
    data = {
        "ip_address": "2620:1ec:21:0:0:0:0:14",
        "netmask": "64",
        "options": {}
    }
    context.o0010 = IPAddress(**data)


@given(u'I create a IPV6 object named o0011')
def step_impl(context):
    context.o0011 = IPV6(
        ip_address="2620:1ec:21:0:0:0:0:14",
        netmask="255.255.255.0",
        options={}
    )


@given(u'I create a wrong IPV6 object named o0012')
def step_impl(context):
    try:
        context.o0012 = IPV6(
            ip_address=NOT_SET,
            netmask=NOT_SET,
            options={}
        )
        assert False
    except ValidationError:
        assert True


@then(u'I can print IPAddress object o0000')
def step_impl(context):
    print(context.o0000)
    print_ip(context.o0000)


@then(u'I can print IPAddress object o0000 in JSON format')
def step_impl(context):
    print("[o0000.to_json()]", context.o0000.to_json())
    print("[o0000.dict()]   ", context.o0000.dict())
    print("")


@then(u'I can print IPV4 object o0001')
def step_impl(context):
    print(context.o0001)
    print_ip(context.o0001)


@then(u'I can print IPV4 object o0001 in JSON format')
def step_impl(context):
    print("[o0001.to_json()]", context.o0001.to_json())
    print("[o0001.dict()]   ", context.o0001.dict())
    print("")


@then(u'I can print IPV4 object o0003 in JSON format')
def step_impl(context):
    print("[o0003.to_json()]", context.o0003.to_json())
    print("[o0003.dict()]   ", context.o0003.dict())
    print("")


@then(u'IPAddress object o0000 is equal to IPV4 object o0001')
def step_impl(context):
    assert context.o0000 == context.o0001


@then(u'I can print IPV6 object o0011')
def step_impl(context):
    print(context.o0011)
    print_ip(context.o0011)


@then(u'I can print IPV6 object o0011 in JSON format')
def step_impl(context):
    print(context.o0011.to_json())
    print(context.o0011.dict())
    print("")


def print_ip(o):
    print(o.ip_address)
    print(o.netmask)
    print("")
