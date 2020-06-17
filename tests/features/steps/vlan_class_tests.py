#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pydantic import ValidationError
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.vlan import VLAN, ListVLAN


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


@then(u'I create a VLAN object to test compare function named o9999')
def step_impl(context):
    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    vlan_lst.vlan_lst.append(
        VLAN(
            id="1",
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
                        ip_address="2001:cafe:0001::1",
                        netmask="64"
                    )
                ]
            ),
            assigned_ports=['swp1', 'swp2', 'swp3'],
            options={}
        )
    )

    vlan_lst.vlan_lst.append(
        VLAN(
            id="999",
            name="management",
            vrf_name="mgmt",
            ipv4_addresses=IPV4Interface(
                ipv4_addresses=[
                    IPV4(
                        ip_address="192.168.10.1",
                        netmask="255.255.255.0"
                    ),
                    IPV4(
                        ip_address="192.168.11.1",
                        netmask="255.255.255.0"
                    )
                ]
            ),
            ipv6_addresses=IPV6Interface(
                ipv6_addresses=[
                    IPV6(
                        ip_address="2001:cafe:0001::1111",
                        netmask="64"
                    )
                ]
            ),
            assigned_ports=['swp1', 'swp2', 'swp3', 'swp4'],
            options={}
        )
    )

    context.o9999 = vlan_lst


@then(u'I create a VLAN object to test compare function with <name> named o9982')
def step_impl(context):
    options = {
        'compare': {
            'name': True
        }
    }
    context.o9982 = create_vlan_obj_for_compare(options)


@then(u'I create a VLAN object to test compare equal to o9982 without <name> named o9983')
def step_impl(context):
    options = {}
    context.o9983 = create_vlan_obj_for_compare(options)


@then(u'I compare VLAN o9982 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9982 != context.o9999


@then(u'I compare VLAN o9983 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9983 == context.o9999


@then(u'I create a VLAN object to test compare function with <vrf_name> named o9984')
def step_impl(context):
    options = {
        'compare': {
            'vrf_name': True
        }
    }
    context.o9984 = create_vlan_obj_for_compare(options)


@then(u'I create a VLAN object to test compare equal to o9984 without <vrf_name> named o9985')
def step_impl(context):
    options = {}
    context.o9985 = create_vlan_obj_for_compare(options)


@then(u'I compare VLAN o9984 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9984 != context.o9999


@then(u'I compare VLAN o9985 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9985 == context.o9999


@then(u'I create a VLAN object to test compare function with <ipv4_addresses> named o9986')
def step_impl(context):
    options = {
        'compare': {
            'ipv4_addresses': True
        }
    }
    context.o9986 = create_vlan_obj_for_compare(options)


@then(u'I create a VLAN object to test compare equal to o9986 without <ipv4_addresses> named o9987')
def step_impl(context):
    options = {}
    context.o9987 = create_vlan_obj_for_compare(options)


@then(u'I compare VLAN o9986 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9986 != context.o9999


@then(u'I compare VLAN o9987 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9987 == context.o9999


@then(u'I create a VLAN object to test compare function with <ipv6_addresses> named o9988')
def step_impl(context):
    options = {
        'compare': {
            'ipv6_addresses': True
        }
    }
    context.o9988 = create_vlan_obj_for_compare(options)


@then(u'I create a VLAN object to test compare equal to o9988 without <ipv6_addresses> named o9989')
def step_impl(context):
    options = {}
    context.o9989 = create_vlan_obj_for_compare(options)


@then(u'I compare VLAN o9988 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9988 != context.o9999


@then(u'I compare VLAN o9989 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9989 == context.o9999


@then(u'I create a VLAN object to test compare function with <assigned_ports> named o9990')
def step_impl(context):
    options = {
        'compare': {
            'assigned_ports': True
        }
    }
    context.o9990 = create_vlan_obj_for_compare(options)


@then(u'I create a VLAN object to test compare equal to o9990 without <assigned_ports> named o9991')
def step_impl(context):
    options = {}
    context.o9991 = create_vlan_obj_for_compare(options)


@then(u'I compare VLAN o9990 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9990 != context.o9999


@then(u'I compare VLAN o9991 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9991 == context.o9999


def create_vlan_obj_for_compare(options={}):
    vlan_lst = ListVLAN(
        vlan_lst=list()
    )

    vlan_lst.vlan_lst.append(
        VLAN(
            id="1",
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
                        ip_address="2001:cafe:0001::1",
                        netmask="64"
                    )
                ]
            ),
            assigned_ports=['swp1', 'swp2', 'swp3'],
            options=options
        )
    )

    vlan_lst.vlan_lst.append(
        VLAN(
            id="999",
            name="NOT_A_GOOD_NAME",
            vrf_name="NOT_A_GOOD_VRF",
            ipv4_addresses=IPV4Interface(
                ipv4_addresses=[
                    IPV4(
                        ip_address="192.168.255.1",
                        netmask="255.255.255.0"
                    ),
                    IPV4(
                        ip_address="192.168.254.1",
                        netmask="255.255.255.0"
                    )
                ]
            ),
            ipv6_addresses=IPV6Interface(
                ipv6_addresses=[
                    IPV6(
                        ip_address="2001:cafe:1234::1111",
                        netmask="64"
                    )
                ]
            ),
            assigned_ports=['swp1', 'swp2', 'swp3', 'swp4', 'NOT_A_PORT?????'],
            options=options
        )
    )

    return vlan_lst
