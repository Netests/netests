#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import ValidationError
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.vlan import VLAN


@given(u'I create a VLAN object named o0000')
def step_impl(context):
    context.o0000 = VLAN(
        id=1,
        name="default",
        vrf_name="default",
        ipv4_addresses=IPV4Interface(
            ipv4_addresses=[
                IPV4(
                    ip_address="192.168.1.1",
                    netmask="255.255.255.0"
                )
            ]
        ),
        ipv6_addresses=IPV6Interface(
            ipv6_addresses=[
                IPV6(
                    ip_address="::1",
                    netmask="128"
                )
            ]
        ),
        assigned_ports=[
            "swp1",
            "swp2"
        ]
    )


@then(u'I can print VLAN object named o0000')
def step_impl(context):
    print(context.o0000)
    print_vlan(context.o0000)


@then(u'I can print VLAN object named o0000 in JSON format')
def step_impl(context):
    context.o0000.print_json()


def print_vlan(o):
    print(o.id)
    print(o.name)
    print(o.vrf_name)
    print(o.ipv4_addresses)
    print(o.ipv6_addresses)
    print(o.assigned_ports)
    print("")
