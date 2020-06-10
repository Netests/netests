#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from behave import given, when, then
from netests.protocols.cdp import CDP, ListCDP
from netests.tools.file import open_json_file, open_txt_file
from netests.comparators.cdp_compare import _compare_cdp
from netests.converters.cdp.cumulus.ssh import _cumulus_cdp_ssh_converter
from netests.converters.cdp.ios.ssh import _ios_cdp_ssh_converter
from netests.converters.cdp.iosxr.ssh import _iosxr_cdp_ssh_converter
from netests.converters.cdp.nxos.api import _nxos_cdp_api_converter
from netests.converters.cdp.nxos.ssh import _nxos_cdp_ssh_converter
from netests.constants import NOT_SET, FEATURES_SRC_PATH, CDP_DATA_HOST_KEY


@given(u'A network protocols named CDP defined in netests/protocols/cdp.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a CDP object equals to Arista manually named o0001')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'I create a CDP object from a Arista API output named o0002')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'I create a CDP object from a Arista Netconf named o0003')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'I create a CDP object from a Arista SSH output named o0004')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'I create a CDP object equals to Cumulus manually named o0101')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )
    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf01",
            local_port="swp3",
            neighbor_port="GigabitEthernet0/0/0/1",
            neighbor_name="ios",
            neighbor_os="Cisco IOS XR Software, Version 6.1.3[Default] Copyright (c) 2017 by Cisco Systems, Inc. running on isco IOS XRv Series",
            neighbor_mgmt_ip="10.1.2.2",
            neighbor_type=['Router']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf01",
            local_port="swp4",
            neighbor_port="GigabitEthernet0/2",
            neighbor_name="leaf05.dh.local",
            neighbor_os="Cisco IOS Software, IOSv Software (VIOS-ADVENTERPRISEK9-M), Version 15.6(1)T, RELEASE SOFTWARE (fc1) Technical Support: http://www.cisco.com/techsupport Copyright (c) 1986-2015 by Cisco Systems, Inc. Compiled Fri 20-Nov-15 13:39 by prod_rel_team running on Cisco",
            neighbor_mgmt_ip="10.1.2.2",
            neighbor_type=['Router']
        )
    )

    context.o0101 = cdp_neighbors_lst


@given(u'I create a CDP object from a Cumulus API output named o0102')
def step_impl(context):
    context.o0102 = _cumulus_cdp_ssh_converter(
        hostname="leaf01",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/cumulus/api/"
                "cumulus_api_get_cdp.json"
            )
        ),
        options={}
    )


@given(u'I create a CDP object from a Cumulus Netconf named o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a Cumulus SSH output named o0104')
def step_impl(context):
    context.o0104 = _cumulus_cdp_ssh_converter(
        hostname="leaf01",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/cumulus/ssh/"
                "cumulus_net_show_lldp.json"
            )
        ),
        options={}
    )


@given(u'I create a CDP object equals to Extreme VSP manually named o0201')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'I create a CDP object from a Extreme VSP API output named o0202')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'I create a CDP object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'I create a CDP object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'I create a CDP object equals to IOS manually named o0301')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf05",
            local_port="GigabitEthernet0/2",
            neighbor_port="swp4",
            neighbor_name="cumulus",
            neighbor_os="Cumulus Linux version 3.7.5",
            neighbor_mgmt_ip="172.16.194.2",
            neighbor_type=['Router']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf05",
            local_port="GigabitEthernet0/1",
            neighbor_port="GigabitEthernet0/0/0/3",
            neighbor_name="ios",
            neighbor_os="Cisco IOS XR Software, Version 6.1.3[Default]",
            neighbor_mgmt_ip=NOT_SET,
            neighbor_type=['Router']
        )
    )

    context.o0301 = cdp_neighbors_lst


@given(u'I create a CDP object from a IOS API output named o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a IOS Netconf named o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a IOS SSH named o0304')
def step_impl(context):
    context.o0304 = _ios_cdp_ssh_converter(
        hostname="leaf05",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/ios/ssh/"
                "ios_show_cdp_neighbors_detail.txt"
            )
        ),
        options={}
    )


@given(u'I create a CDP object equals to IOS-XR manually named o0401')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="eth0",
            neighbor_name="cumulus",
            neighbor_os="Cumulus Linux version 3.7.9",
            neighbor_mgmt_ip="100.96.0.14",
            neighbor_type=['Router']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="mgmt0",
            neighbor_name="leaf02(9OSPMF3QIF6)",
            neighbor_os="Cisco Nexus Operating System(NX-OS) Software, Version 9.2(3)",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router', 'Bridge']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="GigabitEthernet0/0/0/2",
            neighbor_port="GigabitEthernet4",
            neighbor_name="spine02.tesuto.internal",
            neighbor_os="Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router']
        )
    )

    context.o0401 = cdp_neighbors_lst


@given(u'I create a CDP object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a IOS-XR Netconf output named o403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.o0404 = _iosxr_cdp_ssh_converter(
        hostname="spine03",
        cmd_output=open_txt_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/iosxr/ssh/"
                "cisco_iosxr_show_cdp_neighbors_detail.txt"
            )
        ),
        options={}
    )


@given(u'I create a CDP object equals IOS-XR multi manually output named o0405')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a IOS-XR multi Netconf output named o0406')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object equals to Juniper manually named o0501')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'I create a CDP object from a Juniper API output named o0502')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'I create a CDP object from a Juniper Netconf output named o0503')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'I create a CDP object from a Juniper SSH output named o0504')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'I create a CDP object equals to NAPALM manually named o0601')
def step_impl(context):
    print("NAPALM doesn't support CDP")


@given(u'I create a CDP object from a NAPALM output named o0602')
def step_impl(context):
    print("NAPALM doesn't support CDP")


@given(u'I create a CDP object equals to NXOS manually named o0701')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf02",
            local_port="mgmt0",
            neighbor_port="eth0",
            neighbor_name="cumulus",
            neighbor_os="Cumulus Linux version 3.7.5",
            neighbor_mgmt_ip="100.96.0.14",
            neighbor_type=['Router']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf02",
            local_port="mgmt0",
            neighbor_port="GigabitEthernet1",
            neighbor_name="spine02.tesuto.internal",
            neighbor_os="Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by mcpre",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router']
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf02",
            local_port="Ethernet1/2",
            neighbor_port="GigabitEthernet3",
            neighbor_name="spine02.tesuto.internal",
            neighbor_os="Cisco IOS Software [Everest], Virtual XE Software (X86_64_LINUX_IOSD-UNIVERSALK9-M), Version 16.6.1, RELEASE SOFTWARE (fc2)\nTechnical Support: http://www.cisco.com/techsupport\nCopyright (c) 1986-2017 by Cisco Systems, Inc.\nCompiled Sat 22-Jul-17 05:51 by mcpre",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router']
        )
    )

    context.o0701 = cdp_neighbors_lst


@given(u'I create a CDP object from a NXOS API output named o0702')
def step_impl(context):
    context.o0702 = _nxos_cdp_api_converter(
        hostname="leaf02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/nxos/api/"
                "nxos_api_get_cdp_neighbors.json"
            )
        ),
        options={}
    )


@given(u'I create a CDP object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object from a NXOS SSH output named o0704')
def step_impl(context):
    context.o0704 = _nxos_cdp_ssh_converter(
        hostname="leaf02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/nxos/ssh/"
                "nxos_show_cdp_neighbors.json"
            )
        ),
        options={}
    )


@given(u'I create a CDP object equals to NXOS only one manually named o0711')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="leaf02",
            local_port="mgmt0",
            neighbor_port="eth0",
            neighbor_name="cumulus",
            neighbor_os="Cumulus Linux version 3.7.5",
            neighbor_mgmt_ip="100.96.0.14",
            neighbor_type=['Router']
        )
    )

    context.o0711 = cdp_neighbors_lst


@given(u'I create a CDP object from a NXOS only one API output named o0712')
def step_impl(context):
    context.o0712 = _nxos_cdp_api_converter(
        hostname="leaf02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/nxos/api/"
                "nxos_api_get_cdp_neighbors_only_one.json"
            )
        ),
        options={}
    )


@given(u'I create a CDP object from a NXOS only one Netconf output named o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")

@given(u'I create a CDP object from a NXOS only one SSH output named o0714')
def step_impl(context):
    context.o0714 = _nxos_cdp_ssh_converter(
        hostname="leaf02",
        cmd_output=open_json_file(
            path=(
                f"{FEATURES_SRC_PATH}outputs/cdp/nxos/ssh/"
                "nxos_show_cdp_neighbors_only_one.json"
            )
        ),
        options={}
    )


@given(u'CDP o0001 should be equal to o0002')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0001 should be equal to o0003')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0001 should be equal to o0004')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0002 should be equal to o0003')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0002 should be equal to o0004')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0003 should be equal to o0004')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0002')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0003')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0004')
def step_impl(context):
    print("Arista Networks doesn't support CDP")


@given(u'CDP o0101 should be equal to o0102')
def step_impl(context):
    assert context.o0101 == context.o0102


@given(u'CDP o0101 should be equal to o0103')
def step_impl(context):
    print("Cumulus Networks CDP Netconf doesn't exist -> Not tested")


@given(u'CDP o0101 should be equal to o0104')
def step_impl(context):
    assert context.o0101 == context.o0104


@given(u'CDP o0102 should be equal to o0103')
def step_impl(context):
    print("Cumulus Networks CDP Netconf doesn't exist -> Not tested")


@given(u'CDP o0102 should be equal to o0104')
def step_impl(context):
    assert context.o0102 == context.o0104


@given(u'CDP o0103 should be equal to o0104')
def step_impl(context):
    print("Cumulus Networks CDP Netconf doesn't exist -> Not tested")


@given(u'CDP YAML file should be equal to o0102')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['linux'],
        cdp_host_data=context.o0102,
        test=True
    )


@given(u'CDP YAML file should be equal to o0103')
def step_impl(context):
    print("Cumulus Networks CDP Netconf doesn't exist -> Not tested")


@given(u'CDP YAML file should be equal to o0104')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="leaf01",
        groups=['linux'],
        cdp_host_data=context.o0104,
        test=True
    )


@given(u'CDP o0201 should be equal to o0202')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0201 should be equal to o0203')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0201 should be equal to o0204')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0202 should be equal to o0203')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0202 should be equal to o0204')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0203 should be equal to o0204')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP YAML file should be equal to o0202')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP YAML file should be equal to o0203')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP YAML file should be equal to o0204')
def step_impl(context):
    print("Extreme Networks VSP doesn't support CDP")


@given(u'CDP o0301 should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0301 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0301 should be equal to o0304')
def step_impl(context):
    assert context.o0301 == context.o0304


@given(u'CDP o0302 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0302 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0303 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0304')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="leaf05",
        groups=['ios'],
        cdp_host_data=context.o0304,
        test=True
    )


@given(u'CDP o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0401 should be equal to o0404')
def step_impl(context):
    assert (
        context.o0401 == context.o0404 and
        context.o0401.cdp_neighbors_lst[0].local_port == context.o0404.cdp_neighbors_lst[0].local_port and
        context.o0401.cdp_neighbors_lst[0].neighbor_mgmt_ip == context.o0404.cdp_neighbors_lst[0].neighbor_mgmt_ip and
        context.o0401.cdp_neighbors_lst[0].neighbor_name == context.o0404.cdp_neighbors_lst[0].neighbor_name and
        context.o0401.cdp_neighbors_lst[0].neighbor_port == context.o0404.cdp_neighbors_lst[0].neighbor_port and
        context.o0401.cdp_neighbors_lst[0].neighbor_type == context.o0404.cdp_neighbors_lst[0].neighbor_type
    )


@given(u'CDP o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0404')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="spine03",
        groups=['xr'],
        cdp_host_data=context.o0404,
        test=True
    )


@given(u'CDP o0501 should be equal to o0502')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0501 should be equal to o0503')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0501 should be equal to o0504')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0502 should be equal to o0503')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0502 should be equal to o0504')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0503 should be equal to o0504')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0502')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0503')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP YAML file should be equal to o0504')
def step_impl(context):
    print("Juniper Networks doesn't support CDP")


@given(u'CDP o0601 should be equal to o0602')
def step_impl(context):
    print("NAPALM doesn't support CDP")


@given(u'CDP o0701 should be equal to o0702')
def step_impl(context):
    assert (
        context.o0701 == context.o0702 and
        context.o0701.cdp_neighbors_lst[0].local_port == context.o0702.cdp_neighbors_lst[0].local_port and
        context.o0701.cdp_neighbors_lst[0].neighbor_mgmt_ip == context.o0702.cdp_neighbors_lst[0].neighbor_mgmt_ip and
        context.o0701.cdp_neighbors_lst[0].neighbor_name == context.o0702.cdp_neighbors_lst[0].neighbor_name and
        context.o0701.cdp_neighbors_lst[0].neighbor_port == context.o0702.cdp_neighbors_lst[0].neighbor_port and
        context.o0701.cdp_neighbors_lst[0].neighbor_type == context.o0702.cdp_neighbors_lst[0].neighbor_type
    )


@given(u'CDP o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0701 should be equal to o0704')
def step_impl(context):
    assert (
        context.o0701 == context.o0704 and
        context.o0701.cdp_neighbors_lst[0].local_port == context.o0704.cdp_neighbors_lst[0].local_port and
        context.o0701.cdp_neighbors_lst[0].neighbor_mgmt_ip == context.o0704.cdp_neighbors_lst[0].neighbor_mgmt_ip and
        context.o0701.cdp_neighbors_lst[0].neighbor_name == context.o0704.cdp_neighbors_lst[0].neighbor_name and
        context.o0701.cdp_neighbors_lst[0].neighbor_port == context.o0704.cdp_neighbors_lst[0].neighbor_port and
        context.o0701.cdp_neighbors_lst[0].neighbor_type == context.o0704.cdp_neighbors_lst[0].neighbor_type
    )


@given(u'CDP o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0702 should be equal to o0704')
def step_impl(context):
    assert context.o0702 == context.o0702


@given(u'CDP o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0702')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="leaf02",
        groups=['nxos'],
        cdp_host_data=context.o0702,
        test=True
    )


@given(u'CDP YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP YAML file should be equal to o0704')
def step_impl(context):
    assert _compare_cdp(
        host_keys=CDP_DATA_HOST_KEY,
        hostname="leaf02",
        groups=['nxos'],
        cdp_host_data=context.o0704,
        test=True
    )


@given(u'CDP o0711 should be equal to o0712')
def step_impl(context):
    assert (
        context.o0711 == context.o0712 and
        context.o0711.cdp_neighbors_lst[0].local_port == context.o0712.cdp_neighbors_lst[0].local_port and
        context.o0711.cdp_neighbors_lst[0].neighbor_mgmt_ip == context.o0712.cdp_neighbors_lst[0].neighbor_mgmt_ip and
        context.o0711.cdp_neighbors_lst[0].neighbor_name == context.o0712.cdp_neighbors_lst[0].neighbor_name and
        context.o0711.cdp_neighbors_lst[0].neighbor_port == context.o0712.cdp_neighbors_lst[0].neighbor_port and
        context.o0711.cdp_neighbors_lst[0].neighbor_type == context.o0712.cdp_neighbors_lst[0].neighbor_type
    )


@given(u'CDP o0711 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0711 should be equal to o0714')
def step_impl(context):
    assert (
        context.o0711 == context.o0714 and
        context.o0711.cdp_neighbors_lst[0].local_port == context.o0714.cdp_neighbors_lst[0].local_port and
        context.o0711.cdp_neighbors_lst[0].neighbor_mgmt_ip == context.o0714.cdp_neighbors_lst[0].neighbor_mgmt_ip and
        context.o0711.cdp_neighbors_lst[0].neighbor_name == context.o0714.cdp_neighbors_lst[0].neighbor_name and
        context.o0711.cdp_neighbors_lst[0].neighbor_port == context.o0714.cdp_neighbors_lst[0].neighbor_port and
        context.o0711.cdp_neighbors_lst[0].neighbor_type == context.o0714.cdp_neighbors_lst[0].neighbor_type
    )


@given(u'CDP o0712 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'CDP o0712 should be equal to o0714')
def step_impl(context):
    assert context.o0712 == context.o0714


@given(u'CDP o0713 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a CDP object to test compare function named o9999')
def step_impl(context):
    cdp_neighbors_lst = ListCDP(
        cdp_neighbors_lst=list()
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="eth0",
            neighbor_name="leaf01",
            neighbor_os="Cumulus Linux",
            neighbor_mgmt_ip="100.96.0.21",
            neighbor_type=['Router', 'Bridge'],
            options={}
        )
    )

    cdp_neighbors_lst.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="mgmt0",
            neighbor_name="leaf02(9OSPMF3QIF6)",
            neighbor_os="Cisco Nexus Operating System(NX-OS) Software, Version 9.2(3)",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router', 'Bridge'],
            options={}
        )
    )

    context.o9999 = cdp_neighbors_lst


@given(u'I create a CDP object to test compare function with <neighbor_os> named o9982')
def step_impl(context):
    options = {
        'compare': {
            'neighbor_os': True
        }
    }
    context.o9982 = create_cdp_obj_for_compare(options)


@given(u'I create a CDP object to test compare equal to o9982 without <neighbor_os> named o9983')
def step_impl(context):
    options = {}
    context.o9983 = create_cdp_obj_for_compare(options)


@given(u'I compare CDP o9982 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9982 != context.o9999


@given(u'I compare CDP o9983 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9983 == context.o9999


@given(u'I create a CDP object to test compare function with <neighbor_mgmt_ip> named o9984')
def step_impl(context):
    options = {
        'compare': {
            'neighbor_mgmt_ip': True
        }
    }
    context.o9984 = create_cdp_obj_for_compare(options)


@given(u'I create a CDP object to test compare equal to o9984 without <neighbor_mgmt_ip> named o9985')
def step_impl(context):
    options = {}
    context.o9985 = create_cdp_obj_for_compare(options)


@given(u'I compare CDP o9984 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9984 != context.o9999


@given(u'I compare CDP o9985 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9985 == context.o9999


@given(u'I create a CDP object to test compare function with <neighbor_type> named o9986')
def step_impl(context):
    options = {
        'compare': {
            'neighbor_type': True
        }
    }
    context.o9986 = create_cdp_obj_for_compare(options)


@given(u'I create a CDP object to test compare equal to o9986 without <neighbor_type> named o9987')
def step_impl(context):
    options = {}
    context.o9987 = create_cdp_obj_for_compare(options)


@given(u'I compare CDP o9986 and o9999 with a personal function - should not work')
def step_impl(context):
    assert context.o9986 != context.o9999


@given(u'I compare CDP o9987 and o9999 with a personal function - should work')
def step_impl(context):
    assert context.o9987 == context.o9999


def create_cdp_obj_for_compare(options):
    obj = ListCDP(
        cdp_neighbors_lst=list()
    )

    obj.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="eth0",
            neighbor_name="leaf01",
            neighbor_os="NETESTS_IO_IS_CREATING_HIS_OWN_OS...",
            neighbor_mgmt_ip="239.0.0.1__?_MULTICAST_IP_?!!",
            neighbor_type=['BOAT', 'CAR', 'DRUNK'],
            options=options
        )
    )

    obj.cdp_neighbors_lst.append(
        CDP(
            local_name="spine03",
            local_port="MgmtEth0/RP0/CPU0/0",
            neighbor_port="mgmt0",
            neighbor_name="leaf02(9OSPMF3QIF6)",
            neighbor_os="Cisco Nexus Operating System(NX-OS) Software, Version 9.2(3)",
            neighbor_mgmt_ip="100.96.0.20",
            neighbor_type=['Router', 'Bridge'],
            options=options
        )
    )

    return obj



@given(u'I Finish my CDP tests and list tests not implemented')
def step_impl(context):
    context.scenario.tags.append("own_skipped")
