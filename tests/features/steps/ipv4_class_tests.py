#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.ip import IPAddress
from netests.protocols.ipv4 import IPV4


@given(u'I create a IPAddress object named o0000')
def step_impl(context):
    data = {
        "ip_address": "192.168.1.1",
        "netmask": "255.255.255.0"
    }
    context.o0000 = IPAddress(**data)


@given(u'I create a IPV4 object named o0001')
def step_impl(context):
    context.o0001 = IPV4(
        ip_address="192.168.1.1",
        netmask="255.255.255.0"
    )


@then(u'I can print IPAddress object o0000')
def step_impl(context):
    print(context.o0000)
    print_ip(context.o0000)


@then(u'I can print IPAddress object o0000 in JSON format')
def step_impl(context):
    print(context.o0000.to_json())
    print("")


@then(u'I can print IPV4 object o0001')
def step_impl(context):
    print(context.o0001)
    print_ip(context.o0001)


@then(u'I can print IPV4 object o0001 in JSON format')
def step_impl(context):
    print(context.o0001.to_json())
    print("")


@then(u'IPAddress object o0000 is equal to IPV4 object o0001')
def step_impl(context):
    assert context.o0000 == context.o0001


def print_ip(o):
    print(o.ip_address)
    print(o.netmask)
    print("")
