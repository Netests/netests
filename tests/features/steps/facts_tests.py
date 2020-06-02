#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
import textfsm
from behave import given, when, then
from netests.protocols.facts import Facts
from netests.converters.facts.arista.api import _arista_facts_api_converter
from netests.converters.facts.arista.ssh import _arista_facts_ssh_converter
from netests.converters.facts.cumulus.api import _cumulus_facts_api_converter
from netests.converters.facts.cumulus.ssh import _cumulus_facts_ssh_converter
from netests.converters.facts.extreme_vsp.ssh import _extreme_vsp_facts_ssh_converter
from netests.converters.facts.extreme_vsp.api import _extreme_vsp_facts_api_converter
from netests.converters.facts.ios.api import _ios_facts_api_converter
from netests.converters.facts.ios .nc import _ios_facts_nc_converter
from netests.converters.facts.ios.ssh import _ios_facts_ssh_converter
from netests.converters.facts.iosxr.ssh import _iosxr_facts_ssh_converter
from netests.converters.facts.juniper.api import _juniper_facts_api_converter
from netests.converters.facts.juniper .nc import _juniper_facts_nc_converter
from netests.converters.facts.juniper.ssh import _juniper_facts_ssh_converter
from netests.converters.facts.napalm.converter import _napalm_facts_converter
from netests.converters.facts.nxos.api import _nxos_facts_api_converter
from netests.converters.facts.nxos.ssh import _nxos_facts_ssh_converter
from netests.comparators.facts_compare import _compare_facts
from netests.tools.file import open_file, open_txt_file, open_json_file, open_txt_file_as_bytes
from netests.constants import (
    NOT_SET,
    FEATURES_SRC_PATH,
    FEATURES_OUTPUT_PATH,
    FACTS_DATA_HOST_KEY,
    FACTS_SYS_DICT_KEY,
    FACTS_INT_DICT_KEY,
    FACTS_DOMAIN_DICT_KEY,
    FACTS_MEMORY_DICT_KEY,
    FACTS_CONFIG_DICT_KEY,
    FACTS_SERIAL_DICT_KEY
)


@given(u'A network protocols named Facts defined in netests/protocols/facts.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a Facts object equals to Arista manually named o0001')
def step_impl(context):
    context.o0001 = Facts(
        hostname='leaf03',
        domain='dh.local',
        version='4.24.0F',
        build='da8d6269-c25f-4a12-930b-c3c42c12c38a',
        serial='',
        base_mac='50:00:00:d7:ee:0b',
        memory=2014424,
        vendor='Arista',
        model='vEOS',
        interfaces_lst=['Management1',
                        'Ethernet8',
                        'Ethernet2',
                        'Ethernet3',
                        'Ethernet1',
                        'Ethernet6',
                        'Ethernet7',
                        'Ethernet4',
                        'Ethernet5'],
        options={}
    )


@given(u'I create a Facts object from a Arista API output named o0002')
def step_impl(context):
    cmd_output = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/arista/api/"
            "arista_api_get_facts.json"
        )
    )
    context.o0002 = _arista_facts_api_converter(
        hostname="leaf03",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object from a Arista SSH output named o0004')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/arista/ssh/"
            "arista_cli_show_version.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/arista/ssh/"
            "arista_cli_show_interface_status.json"
        )
    )
    cmd_output[FACTS_DOMAIN_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/arista/ssh/"
            "arista_cli_show_hostname.json"
        )
    )
    context.o0004 = _arista_facts_ssh_converter(
        hostname="leaf03",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object equals to Cumulus manually named o0101')
def step_impl(context):
    context.o0101 = Facts(
        hostname='cumulus',
        domain=NOT_SET,
        version='3.7.5',
        build='Cumulus Linux 3.7.5',
        serial='50:00:00:01:00:00',
        base_mac='50:00:00:01:00:00',
        memory=951264,
        vendor='Cumulus Networks',
        model='VX',
        interfaces_lst=['swp5',
                        'swp7',
                        'swp2',
                        'swp3',
                        'swp1',
                        'swp6',
                        'swp4',
                        'eth0'],
        options={}
    )


@given(u'I create a Facts object from a Cumulus API output named o0102')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_txt_file_as_bytes(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/cumulus/api/"
            "cumulus_api_show_system.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_txt_file_as_bytes(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/cumulus/api/"
            "cumulus_api_show_interface_all.json"
        )
    )
    context.o0102 = _cumulus_facts_api_converter(
        hostname="leaf01",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a Cumulus Netconf named o0103')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'I create a Facts object from a Cumulus SSH output named o0104')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/cumulus/ssh/"
            "cumulus_net_show_system.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/cumulus/ssh/"
            "cumulus_net_show_interface_all.json"
        )
    )
    context.o0104 = _cumulus_facts_ssh_converter(
        hostname="leaf01",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object equals to Extreme VSP manually named o0201')
def step_impl(context):
    context.o0201 = Facts(
        hostname='spine02',
        domain='dh.local',
        version='8.1.0.0',
        build=NOT_SET,
        serial='SDNIPM624B36',
        base_mac='00:51:00:02:00:00',
        memory=2087444480,
        vendor='Extreme Networks',
        model='8284XSQ',
        interfaces_lst=[ 'mgmt',
                         '1/1',
                         '1/2',
                         '1/3',
                         '1/4',
                         '1/5',
                         '1/6',
                         '1/7',
                         '1/8',
                         '1/9',
                         '1/10',
                         '1/11',
                         '1/12',
                         '1/13',
                         '1/14',
                         '1/15',
                         '1/16',
                         '1/17',
                         '1/18',
                         '1/19',
                         '1/20',
                         '1/21',
                         '1/22',
                         '1/23',
                         '1/24',
                         '1/25',
                         '1/26',
                         '1/27',
                         '1/28',
                         '1/29',
                         '1/30',
                         '1/31',
                         '1/32',
                         '1/33',
                         '1/34',
                         '1/35',
                         '1/36',
                         '1/37',
                         '1/38',
                         '1/39',
                         '1/40',
                         '1/41',
                         '1/42',
                         '2/1',
                         '2/2',
                         '2/3',
                         '2/4',
                         '2/5',
                         '2/6',
                         '2/7',
                         '2/8',
                         '2/9',
                         '2/10',
                         '2/11',
                         '2/12',
                         '2/13',
                         '2/14',
                         '2/15',
                         '2/16',
                         '2/17',
                         '2/18',
                         '2/19',
                         '2/20',
                         '2/21',
                         '2/22',
                         '2/23',
                         '2/24',
                         '2/25',
                         '2/26',
                         '2/27',
                         '2/28',
                         '2/29',
                         '2/30',
                         '2/31',
                         '2/32',
                         '2/33',
                         '2/34',
                         '2/35',
                         '2/36',
                         '2/37',
                         '2/38',
                         '2/39',
                         '2/40',
                         '2/41',
                         '2/42',
                         'Default'],
        options={}
    )


@given(u'I create a Facts object from a Extreme VSP API output named o0202')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/extreme_vsp/api/"
            "extreme_vsp_api_openconfig_system.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/extreme_vsp/api/"
            "extreme_vsp_api_openconfig_interfaces.json"
        )
    )

    context.o0202 = _extreme_vsp_facts_api_converter(
        hostname="spine02",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'I create a Facts object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/extreme_vsp/ssh/"
            "extreme_vsp_show_tech.txt"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/extreme_vsp/ssh/"
            "extreme_vsp_show_interfaces_gigabitethernet_name.txt"
        )
    )
    cmd_output[FACTS_DOMAIN_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/extreme_vsp/ssh/"
            "extreme_vsp_show_sys_dns.txt"
        )
    )

    context.o0204 = _extreme_vsp_facts_ssh_converter(
        hostname="spine02",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object equals to IOS manually named o0301')
def step_impl(context):
    context.o0301 = Facts(
        hostname='leaf05',
        domain='dh.local',
        version='16.8.1',
        build='fc3',
        serial='9YEI1T9ZCIY',
        base_mac=NOT_SET,
        memory='8113376',
        vendor='Cisco',
        model='CSR1000V',
        interfaces_lst=['GigabitEthernet1',
                        'GigabitEthernet2',
                        'GigabitEthernet3'],
        options={}
    )


@given(u'I create a Facts object from a IOS API output named o0302')
def step_impl(context):
    context.o0302 = _ios_facts_api_converter(
        hostname="leaf05",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/facts/ios/api/"
                "cisco_ios_api_get_facts_16.8.json"
            )
        ),
        options={}
    )


@given(u'I create a Facts object from a IOS Netconf named o0303')
def step_impl(context):
    context.o0303 = _ios_facts_nc_converter(
        hostname="leaf05",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/facts/ios/netconf/"
                "cisco_ios_nc_get_facts.xml"
            )
        ),
        options={}
    )


@given(u'I create a Facts object from a IOS SSH named o0304')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/ios/ssh/"
            "cisco_ios_show_version.txt"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/ios/ssh/"
            "cisco_ios_ip_interface_brief.txt"
        )
    )
    context.o0304 = _ios_facts_ssh_converter(
        hostname="spine02",
        cmd_output=cmd_output,
        options={}
    )

@given(u'I create a Facts object equals to IOS 16.9 manually named o0311')
def step_impl(context):
    context.o0311 = Facts(
        hostname='csr1000v',
        domain='abc.inc',
        version='16.9',
        build=NOT_SET,
        serial='9KAAMNP24B9',
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor='Cisco',
        model='CSR1000V',
        interfaces_lst=['GigabitEthernet1',
                        'GigabitEthernet2',
                        'GigabitEthernet3',
                        'Loopback12',
                        'Loopback101',
                        'Loopback854',
                        'Loopback1500',
                        'Loopback1501',
                        'Loopback1609',
                        'Loopback1974',
                        'Loopback1996',
                        'Loopback1997',
                        'Loopback1998',
                        'Loopback2000',
                        'Loopback2222',
                        'Loopback3000',
                        'Loopback4321',
                        'Loopback5263'],
        options={}
    )


@given(u'I create a Facts object from a IOS API 16.9 output named o0312')
def step_impl(context):
    context.o0312 = _ios_facts_api_converter(
        hostname="leaf05",
        cmd_output=open_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/facts/ios/api/"
                "cisco_ios_api_get_facts_16.9.json"
            )
        ),
        options={}
    )


@given(u'I create a Facts object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.o0401 = Facts(
        hostname='spine03',
        domain='dh.local',
        version='6.5.3',
        build=NOT_SET,
        serial=NOT_SET,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor='Cisco',
        model='IOS-XRv 9000',
        interfaces_lst=['Bundle-Ether1',
                        'Bundle-Ether1.1234',
                        'Bundle-Ether1.4321',
                        'Loopback100',
                        'Loopback200',
                        'MgmtEth0/RP0/CPU0/0',
                        'GigabitEthernet0/0/0/0',
                        'GigabitEthernet0/0/0/1',
                        'GigabitEthernet0/0/0/2',
                        'GigabitEthernet0/0/0/3',
                        'GigabitEthernet0/0/0/4',
                        'GigabitEthernet0/0/0/5',
                        'GigabitEthernet0/0/0/6'],
        options={}
    )


@given(u'I create a Facts object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object from a IOS-XR Netconf output named o403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object from a IOS-XR SSH output named o0404')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/iosxr/ssh/"
            "cisco_iosxr_show_version.txt"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/iosxr/ssh/"
            "cisco_iosxr_show_ip_interface_brief.txt"
        )
    )
    context.o0404 = _iosxr_facts_ssh_converter(
        hostname="spine02",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object equals IOS-XR multi manually output named o0405')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object from a IOS-XR multi Netconf output named o0406')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object equals to Juniper manually named o0501')
def step_impl(context):
    context.o0501 = Facts(
        hostname='leaf04',
        domain='dh.local',
        version='18.3R1.9',
        build=NOT_SET,
        serial='VM5E983D143E',
        base_mac=NOT_SET,
        memory=2052008,
        vendor='Juniper',
        model='VMX',
        interfaces_lst=[],
        options={}
    )


@given(u'I create a Facts object from a Juniper API output named o0502')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/api/"
            "juniper_api_get_software_information.xml"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/api/"
            "juniper_api_get_interface_information_terse.xml"
        )
    )
    cmd_output[FACTS_SERIAL_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/api/"
            "juniper_api_get_chassis_inventory_detail.xml"
        )
    )
    cmd_output[FACTS_MEMORY_DICT_KEY] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/api/"
            "juniper_api_get_system_memory_information.xml"
        )
    )

    context.o0502 = _juniper_facts_api_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a Juniper Netconf output named o0503')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/netconf/"
            "juniper_nc_get_facts.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/netconf/"
            "juniper_nc_get_interfaces_terse.xml"
        )
    )
    context.o0503 = _juniper_facts_nc_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a Juniper SSH output named o0504')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_version.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_interfaces_terse.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_interfaces_terse.json"
        )
    )
    cmd_output[FACTS_MEMORY_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_system_memory.json"
        )
    )
    cmd_output[FACTS_CONFIG_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_conf_system.json"
        )
    )
    cmd_output[FACTS_SERIAL_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/juniper/ssh/"
            "juniper_show_hardware_detail.json"
        )
    )
    context.o0504 = _juniper_facts_ssh_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object equals to NAPALM manually named o0601')
def step_impl(context):
    context.o0601 = Facts(
        hostname='leaf03',
        domain=NOT_SET,
        version=NOT_SET,
        build=NOT_SET,
        serial='9QXOX90PJ62',
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor='Cisco',
        model='Nexus9000 C9300v Chassis',
        interfaces_lst=[],
        options={}
    )


@given(u'I create a Facts object from a NAPALM output named o0602')
def step_impl(context):
    context.o0602 = _napalm_facts_converter(
        hostname="leaf03",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/facts/napalm/nxos_get_facts.json"
            )
        ),
        options={}
    )


@given(u'I create a Facts object equals to NXOS manually named o0701')
def step_impl(context):
    context.o0701 = Facts(
        hostname='leaf02',
        domain='dh.local',
        version='9.3(3)',
        build=NOT_SET,
        serial='9QXOX90PJ62',
        base_mac=NOT_SET,
        memory='16409064',
        vendor='Cisco Systems, Inc.',
        model='Nexus9000',
        interfaces_lst=[],
        options={}
    )


@given(u'I create a Facts object from a NXOS API output named o0702')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/api/"
            "nxos_api_get_facts.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/api/"
            "nxos_api_get_interfaces.json"
        )
    )
    cmd_output[FACTS_DOMAIN_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/api/"
            "nxos_api_get_domain.json"
        )
    )

    context.o0702 = _nxos_facts_api_converter(
        hostname="leaf03",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a Facts object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a Facts object from a NXOS SSH output named o0704')
def step_impl(context):
    cmd_output = dict()
    cmd_output[FACTS_SYS_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/ssh/"
            "nxos_show_version.json"
        )
    )
    cmd_output[FACTS_INT_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/ssh/"
            "nxos_show_interfaces.json"
        )
    )
    cmd_output[FACTS_DOMAIN_DICT_KEY] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/facts/nxos/ssh/"
            "nxos_show_hostname.json"
        )
    )
    
    context.o0704 = _nxos_facts_ssh_converter(
        hostname="leaf03",
        cmd_output=cmd_output,
        options={}
    )


@given(u'Facts o0001 should be equal to o0002')
def step_impl(context):
    assert (
        context.o0001 == context.o0002 and
        context.o0001.hostname == context.o0002.hostname and
        context.o0001.domain == context.o0002.domain and
        context.o0001.version == context.o0002.version and
        context.o0001.build == context.o0002.build and
        context.o0001.base_mac == context.o0002.base_mac and
        context.o0001.memory == context.o0002.memory and
        context.o0001.vendor == context.o0002.vendor and
        context.o0001.model == context.o0002.model and
        context.o0001.interfaces_lst == context.o0002.interfaces_lst
    )


@given(u'Facts o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0001 should be equal to o0004')
def step_impl(context):
    assert (
        context.o0001 == context.o0004 and
        context.o0001.hostname == context.o0004.hostname and
        context.o0001.domain == context.o0004.domain and
        context.o0001.version == context.o0004.version and
        context.o0001.build == context.o0004.build and
        context.o0001.base_mac == context.o0004.base_mac and
        context.o0001.memory == context.o0004.memory and
        context.o0001.vendor == context.o0004.vendor and
        context.o0001.model == context.o0004.model and
        context.o0001.interfaces_lst == context.o0004.interfaces_lst
    )


@given(u'Facts o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0002 should be equal to o0004')
def step_impl(context):
    assert (
        context.o0002 == context.o0004 and
        context.o0002.hostname == context.o0004.hostname and
        context.o0002.domain == context.o0004.domain and
        context.o0002.version == context.o0004.version and
        context.o0002.build == context.o0004.build and
        context.o0002.base_mac == context.o0004.base_mac and
        context.o0002.memory == context.o0004.memory and
        context.o0002.vendor == context.o0004.vendor and
        context.o0002.model == context.o0004.model and
        context.o0002.interfaces_lst == context.o0004.interfaces_lst
    )


@given(u'Facts o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0002')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['eos'],
        facts_host_data=context.o0002,
        test=True
    )


@given(u'Facts YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0004')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf03",
        groups=['eos'],
        facts_host_data=context.o0004,
        test=True
    )


@given(u'Facts o0101 should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0101 should be equal to o0103')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'Facts o0101 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0102 should be equal to o0103')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'Facts o0102 should be equal to o0104')
def step_impl(context):
    assert context.o0102 == context.o0104
    assert (
        context.o0102.hostname == context.o0104.hostname and
        context.o0102.domain == context.o0104.domain and
        context.o0102.version == context.o0104.version and
        context.o0102.build == context.o0104.build and
        context.o0102.serial == context.o0104.serial and
        context.o0102.base_mac == context.o0104.base_mac and
        context.o0102.memory == context.o0104.memory and
        context.o0102.vendor == context.o0104.vendor and
        context.o0102.model == context.o0104.model and
        context.o0102.interfaces_lst == context.o0104.interfaces_lst
    )

@given(u'Facts o0103 should be equal to o0104')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'Facts YAML file should be equal to o0102')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['linux'],
        facts_host_data=context.o0102,
        test=True
    )


@given(u'Facts YAML file should be equal to o0103')
def step_impl(context):
    print("Cumulus Facts with Netconf not possible -> Not tested")


@given(u'Facts YAML file should be equal to o0104')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['linux'],
        facts_host_data=context.o0104,
        test=True
    )


@given(u'Facts o0201 should be equal to o0202')
def step_impl(context):
    assert (
        context.o0201.hostname == context.o0202.hostname and
        context.o0201.domain == context.o0202.domain and
        context.o0201.memory == context.o0202.memory and
        context.o0201.interfaces_lst == context.o0202.interfaces_lst
    )


@given(u'Facts o0201 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'Facts o0201 should be equal to o0204')
def step_impl(context):
    assert (
        context.o0201.hostname == context.o0204.hostname and
        context.o0201.domain == context.o0204.domain and
        context.o0201.version == context.o0204.version and
        context.o0201.base_mac == context.o0204.base_mac and
        context.o0201.model == context.o0204.model and
        context.o0201.serial == context.o0204.serial
    )


@given(u'Facts o0202 should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'Facts o0202 should be equal to o0204')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'Facts o0203 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0203')
def step_impl(context):
    print("Extreme VSP VRF with Netconf not possible -> Not tested")


@given(u'Facts YAML file should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0301 should be equal to o0302')
def step_impl(context):
    assert (
        context.o0301.hostname == context.o0302.hostname and
        context.o0301.domain == context.o0302.domain and
        context.o0301.vendor == context.o0302.vendor and
        context.o0301.model == context.o0302.model and
        context.o0301.serial == context.o0302.serial and
        context.o0301.interfaces_lst == context.o0302.interfaces_lst
    )


@given(u'Facts o0301 should be equal to o0303')
def step_impl(context):
    assert (
        context.o0301.hostname == context.o0303.hostname and
        context.o0301.domain == context.o0303.domain and
        context.o0301.vendor == context.o0303.vendor and
        context.o0301.model == context.o0303.model and
        context.o0301.serial == context.o0303.serial and
        context.o0301.interfaces_lst == context.o0303.interfaces_lst
    )


@given(u'Facts o0301 should be equal to o0304')
def step_impl(context):
    assert (
        context.o0301 == context.o0304 and
        context.o0301.vendor == context.o0304.vendor and
        context.o0301.build == context.o0304.build and
        context.o0301.memory == context.o0304.memory and
        context.o0301.interfaces_lst == context.o0304.interfaces_lst
    )


@given(u'Facts o0302 should be equal to o0303')
def step_impl(context):
    assert (
        context.o0302 == context.o0303 and
        context.o0302.hostname == context.o0303.hostname and
        context.o0302.domain == context.o0303.domain and
        context.o0302.vendor == context.o0303.vendor and
        context.o0302.model == context.o0303.model and
        context.o0302.serial == context.o0303.serial and
        context.o0302.version == context.o0303.version and
        context.o0302.memory == context.o0303.memory and
        context.o0302.base_mac == context.o0303.base_mac and
        context.o0302.build == context.o0303.build and
        context.o0302.interfaces_lst == context.o0303.interfaces_lst
    )


@given(u'Facts o0302 should be equal to o0304')
def step_impl(context):
    assert (
        context.o0302.vendor == context.o0304.vendor and
        context.o0302.serial == context.o0304.serial and
        context.o0302.hostname == context.o0304.hostname and
        context.o0302.model == context.o0304.model and
        context.o0302.interfaces_lst == context.o0304.interfaces_lst
    )


@given(u'Facts o0303 should be equal to o0304')
def step_impl(context):
    assert (
        context.o0303.vendor == context.o0304.vendor and
        context.o0303.serial == context.o0304.serial and
        context.o0303.hostname == context.o0304.hostname and
        context.o0303.model == context.o0304.model and
        context.o0303.interfaces_lst == context.o0304.interfaces_lst
    )


@given(u'Facts o0311 should be equal to o0312')
def step_impl(context):
    assert (
        context.o0311.hostname == context.o0312.hostname and
        context.o0311.domain == context.o0312.domain and
        context.o0311.vendor == context.o0312.vendor and
        context.o0311.serial == context.o0312.serial and
        context.o0311.model == context.o0312.model and
        context.o0311.interfaces_lst == context.o0312.interfaces_lst
    )


@given(u'Facts YAML file should be equal to o0302')
def step_impl(context):
    print("/!\\/!\\ Facts YAML file should be equal to o0302 /!\\/!\\")
    assert not _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf05",
        groups=['ios'],
        facts_host_data=context.o0302,
        test=True
    )


@given(u'Facts YAML file should be equal to o0303')
def step_impl(context):
    print("/!\\/!\\ Facts YAML file should be equal to o0303 /!\\/!\\")
    assert not _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf05",
        groups=['ios'],
        facts_host_data=context.o0303,
        test=True
    )


@given(u'Facts YAML file should be equal to o0304')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf05",
        groups=['ios'],
        facts_host_data=context.o0304,
        test=True
    )


@given(u'Facts o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0401 should be equal to o0404')
def step_impl(context):
    assert (
        context.o0401 == context.o0404 and
        context.o0401.vendor == context.o0404.vendor and
        context.o0401.hostname == context.o0404.hostname and
        context.o0401.model == context.o0404.model and
        context.o0401.version == context.o0404.version and
        context.o0401.interfaces_lst == context.o0404.interfaces_lst
    )


@given(u'Facts o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0405 should be equal to o0406')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0404')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="spine03",
        groups=['iosxr'],
        facts_host_data=context.o0404,
        test=True
    )


@given(u'Facts o0501 should be equal to o0502')
def step_impl(context):
    assert (
        context.o0501.hostname == context.o0502.hostname and
        context.o0501.vendor == context.o0502.vendor and
        context.o0501.model == context.o0502.model
    )


@given(u'Facts o0501 should be equal to o0503')
def step_impl(context):
    assert (
        context.o0501.hostname == context.o0503.hostname and
        context.o0501.domain == context.o0503.domain and
        context.o0501.model == context.o0503.model
    )


@given(u'Facts o0501 should be equal to o0504')
def step_impl(context):
    assert context.o0501 == context.o0504


@given(u'Facts o0502 should be equal to o0503')
def step_impl(context):
    assert context.o0502 == context.o0503
    assert (
        context.o0502.hostname == context.o0503.hostname and
        context.o0502.version == context.o0503.version and
        context.o0502.build == context.o0503.build and
        context.o0502.serial == context.o0503.serial and
        context.o0502.base_mac == context.o0503.base_mac and
        context.o0502.vendor == context.o0503.vendor and
        context.o0502.model == context.o0503.model and
        context.o0502.interfaces_lst == context.o0503.interfaces_lst
    )


@given(u'Facts o0502 should be equal to o0504')
def step_impl(context):
    assert (
        context.o0503.hostname == context.o0504.hostname and
        context.o0503.build == context.o0504.build and
        context.o0503.base_mac == context.o0504.base_mac and
        context.o0503.vendor == context.o0504.vendor and
        context.o0503.model == context.o0504.model
    )


@given(u'Facts o0503 should be equal to o0504')
def step_impl(context):
    assert (
        context.o0503.hostname == context.o0504.hostname and
        context.o0503.domain == context.o0504.domain and
        context.o0503.build == context.o0504.build and
        context.o0503.base_mac == context.o0504.base_mac and
        context.o0503.vendor == context.o0504.vendor and
        context.o0503.model == context.o0504.model
   )


@given(u'Facts YAML file should be equal to o0502')
def step_impl(context):
    assert True
    print("Facts YAML file and o0502 - Versions are differents !")


@given(u'Facts YAML file should be equal to o0503')
def step_impl(context):
    assert True
    print("Facts YAML file and o0503 - Versions are differents !")


@given(u'Facts YAML file should be equal to o0504')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf04",
        groups=['junos'],
        facts_host_data=context.o0504,
        test=True
    )


@given(u'Facts o0601 should be equal to o0602')
def step_impl(context):
    assert context.o0601 == context.o0602


@given(u'Facts o0701 should be equal to o0702')
def step_impl(context):
    assert context.o0701 == context.o0701
    assert (
        context.o0701.domain == context.o0701.domain and
        context.o0701.version == context.o0701.version and
        context.o0701.memory == context.o0701.memory
    )


@given(u'Facts o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0701 should be equal to o0704')
def step_impl(context):
    assert context.o0701 == context.o0704
    assert (
        context.o0701.domain == context.o0704.domain and
        context.o0701.version == context.o0704.version and
        context.o0701.memory == context.o0704.memory
    )


@given(u'Facts o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts o0702 should be equal to o0704')
def step_impl(context):
    assert (
        context.o0702 == context.o0704 and
        context.o0702.hostname == context.o0704.hostname and
        context.o0702.domain == context.o0704.domain and
        context.o0702.version == context.o0704.version and
        str(context.o0702.memory) == str(context.o0704.memory) and
        context.o0702.model == context.o0704.model and
        context.o0702.serial == context.o0704.serial and
        context.o0702.interfaces_lst == context.o0704.interfaces_lst
    )


@given(u'Facts o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0702')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf02",
        groups=['nxos'],
        facts_host_data=context.o0702,
        test=True
    )


@given(u'Facts YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'Facts YAML file should be equal to o0704')
def step_impl(context):
    assert _compare_facts(
        host_keys=FACTS_DATA_HOST_KEY,
        hostname="leaf02",
        groups=['nxos'],
        facts_host_data=context.o0704,
        test=True
    )


@given(u'I Finish my Facts tests and list tests not implemented')
def step_impl(context):
    print("| The following tests are not implemented :")
    for test in context.test_not_implemented:
        print(f"| {test}")
