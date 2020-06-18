#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from behave import given, when, then
from netests.comparators.vlan_compare import _compare_vlan
from netests.protocols.ipv4 import IPV4, IPV4Interface
from netests.protocols.ipv6 import IPV6, IPV6Interface
from netests.protocols.vlan import VLAN, ListVLAN
from netests.converters.vlan.cumulus.ssh import _cumulus_vlan_ssh_converter
from netests.constants import NOT_SET, VLAN_DATA_HOST_KEY, FEATURES_SRC_PATH
from netests.tools.file import open_file, open_json_file


@given(u'A network protocols named VLAN defined in netests/protocols/vlan.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a VLAN object equals to Arista manually named o0001')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Arista API output named o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Arista SSH output named o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to Cumulus manually named o0101')
def step_impl(context):
    context.o0101 = ListVLAN(
        vlan_lst=list()
    )

    context.o0101.vlan_lst.append(
        VLAN(
            id="999",
            name="NETESTS_VLAN_MGMT",
            vrf_name=NOT_SET,
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
                        ip_address="2001:cafe::1",
                        netmask="64"
                    )
                ]
            ),
            assigned_ports=['swp1', 'swp2', 'swp3'],
            options={}
        )
    )


@given(u'I create a VLAN object from a Cumulus API output named o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Cumulus Netconf named o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Cumulus SSH output named o0104')
def step_impl(context):
    context.o0104 = _cumulus_vlan_ssh_converter(
        hostname="leaf01",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/vlan/cumulus/ssh/"
                "cumulus_ssh_net_show_interface_all.json"
            )
        ),
        options={}
    )


@given(u'I create a VLAN object equals to Extreme VSP manually named o0201')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Extreme VSP API output named o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to IOS manually named o0301')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS API output named o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS Netconf named o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS SSH named o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS-XR Netconf output named o403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to Juniper manually named o0501')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Juniper API output named o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Juniper Netconf output named o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a Juniper SSH output named o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to NAPALM manually named o0601')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NAPALM output named o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to NXOS manually named o0701')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS API output named o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS SSH output named o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object equals to NXOS only one manually named o0711')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS only one API output named o0712')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS only one Netconf output named o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a VLAN object from a NXOS only one SSH output named o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0001 should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0001 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0002 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0101 should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0101 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0101 should be equal to o0104')
def step_impl(context):
    assert context.o0101 == context.o0104


@given(u'VLAN o0102 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0102 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0103 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0104')
def step_impl(context):
    assert _compare_vlan(
        host_keys=VLAN_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['linux'],
        vlan_host_data=context.o0104,
        test=True
    )


@given(u'VLAN o0201 should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0201 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0201 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0202 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0202 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0203 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0301 should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0301 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0301 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0302 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0302 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0303 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0401 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0501 should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0501 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0501 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0502 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0502 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0503 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0601 should be equal to o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0701 should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0701 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0702 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN YAML file should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0711 should be equal to o0712')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0711 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0711 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0712 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0712 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'VLAN o0713 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I Finish my VLAN tests and list tests not implemented')
def step_impl(context):
    print("| The following tests are not implemented :")
    for test in context.test_not_implemented:
        print(f"| {test}")
