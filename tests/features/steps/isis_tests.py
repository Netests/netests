#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.comparators.isis_compare import _compare_isis
from netests.converters.isis.juniper.api import _juniper_isis_api_converter
from netests.converters.isis.juniper.nc import _juniper_isis_nc_converter
from netests.converters.isis.juniper.ssh import _juniper_isis_ssh_converter
from netests.constants import NOT_SET, FEATURES_SRC_PATH, ISIS_DATA_HOST_KEY
from netests.tools.file import open_json_file, open_txt_file, open_txt_file_as_bytes
from netests.protocols.isis import (
    ISISAdjacency,
    ListISISAdjacency,
    ISISAdjacencyVRF,
    ListISISAdjacencyVRF,
    ISIS
)

@given(u'A network protocols named ISIS defined in netests/protocols/isis.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a ISIS object equals to Arista manually named o0001')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Arista API output named o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Arista SSH output named o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to Cumulus manually named o0101')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Cumulus API output named o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Cumulus Netconf named o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Cumulus SSH output named o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to Extreme VSP manually named o0201')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Extreme VSP API output named o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to IOS manually named o0301')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS API output named o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS Netconf named o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS SSH named o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS-XR Netconf output named o403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to Juniper manually named o0501')
def step_impl(context):

    isis_vrf_lst = ListISISAdjacencyVRF(
        isis_vrf_lst=list()
    )

    isis_adj_lst = ListISISAdjacency(
        isis_adj_lst=list()
    )

    isis_adj_lst.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type="level-2",
            circuit_type="2",
            local_interface_name="ge-0/0/1.0",
            neighbor_sys_name="vMX5",
            neighbor_ip_addr="10.100.15.2",
            snap="0:50:56:a2:e8:28"
        )
    )

    isis_adj_lst.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type="level-2",
            circuit_type="2",
            local_interface_name="ge-0/0/2.0",
            neighbor_sys_name="vMX2",
            neighbor_ip_addr="10.100.12.2",
            snap="0:50:56:a2:bd:1a"
        )
    )

    isis_adj_lst.isis_adj_lst.append(
        ISISAdjacency(
            session_state="Up",
            level_type="level-2",
            circuit_type="2",
            local_interface_name="ge-0/0/0.0",
            neighbor_sys_name="vMX3",
            neighbor_ip_addr="10.100.13.2",
            snap="0:50:56:a2:8a:cb"
        )
    )

    isis_vrf_lst.isis_vrf_lst.append(
         ISISAdjacencyVRF(
            router_id="10.100.100.1",
            system_id="1010.0100.0001",
            area_id="49.0001",
            vrf_name="default",
            adjacencies=isis_adj_lst
        )
     )

    context.o0501 = ISIS(
        isis_vrf_lst=isis_vrf_lst
    )


@given(u'I create a ISIS object from a Juniper API output named o0502')
def step_impl(context):
    cmd_output = dict()
    cmd_output['default'] = dict()
    cmd_output['default']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/api/"
            "juniper_get_isis_overview.xml"
        )
    )
    cmd_output['default']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/api/"
            "juniper_get_isis_adjacencies.xml"
        )
    )
    cmd_output['mgmt_junos'] = dict()
    cmd_output['mgmt_junos']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/api/"
            "juniper_get_isis_overview_mgmt_empty.xml"
        )
    )
    cmd_output['mgmt_junos']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/api/"
            "juniper_get_isis_adjacencies_mgmt_empty.xml"
        )
    )
    context.o0502 = _juniper_isis_api_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a ISIS object from a Juniper Netconf output named o0503')
def step_impl(context):
    cmd_output = dict()
    cmd_output['default'] = dict()
    cmd_output['default']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/nc/"
            "juniper_get_isis_overview.xml"
        )
    )
    cmd_output['default']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/nc/"
            "juniper_get_isis_adjacencies.xml"
        )
    )
    cmd_output['mgmt_junos'] = dict()
    cmd_output['mgmt_junos']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/nc/"
            "juniper_get_isis_overview_mgmt_empty.xml"
        )
    )
    cmd_output['mgmt_junos']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/nc/"
            "juniper_get_isis_adjacencies_mgmt_empty.xml"
        )
    )
    context.o0503 = _juniper_isis_nc_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    ) 


@given(u'I create a ISIS object from a Juniper SSH output named o0504')
def step_impl(context):
    cmd_output = dict()
    cmd_output['default'] = dict()
    cmd_output['default']['rid'] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/ssh/"
            "juniper_get_isis_overview.json"
        )
    )
    cmd_output['default']['data'] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/ssh/"
            "juniper_get_isis_adjacencies.json"
        )
    )
    cmd_output['mgmt_junos'] = dict()
    cmd_output['mgmt_junos']['rid'] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/ssh/"
            "juniper_get_isis_overview_mgmt_empty.json"
        )
    )
    cmd_output['mgmt_junos']['data'] = open_json_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/isis/juniper/ssh/"
            "juniper_get_isis_adjacencies_mgmt_empty.json"
        )
    )
    context.o0504 = _juniper_isis_ssh_converter(
        hostname="leaf04",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a ISIS object equals to NAPALM manually named o0601')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NAPALM output named o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to NXOS manually named o0701')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS API output named o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS SSH output named o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object equals to NXOS only one manually named o0711')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS only one API output named o0712')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS only one Netconf output named o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a ISIS object from a NXOS only one SSH output named o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0001 should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0001 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0002 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0101 should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0101 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0101 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0102 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0102 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0103 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0201 should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0201 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0201 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0202 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0202 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0203 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0301 should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0301 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0301 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0302 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0302 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0303 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0401 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0501 should be equal to o0502')
def step_impl(context):
    context.o0501 == context.o0502


@given(u'ISIS o0501 should be equal to o0503')
def step_impl(context):
    context.o0501 == context.o0503


@given(u'ISIS o0501 should be equal to o0504')
def step_impl(context):
    context.o0501 == context.o0504


@given(u'ISIS o0502 should be equal to o0503')
def step_impl(context):
    context.o0502 == context.o0503


@given(u'ISIS o0502 should be equal to o0504')
def step_impl(context):
    context.o0502 == context.o0504


@given(u'ISIS o0503 should be equal to o0504')
def step_impl(context):
    context.o0503 == context.o0504


@given(u'ISIS YAML file should be equal to o0502')
def step_impl(context):
    _compare_isis(
        host_keys=ISIS_DATA_HOST_KEY,
        hostname='leaf04',
        groups=['junos'],
        isis_host_data=context.o0502,
        test=True,
        options={}
    )


@given(u'ISIS YAML file should be equal to o0503')
def step_impl(context):
    _compare_isis(
        host_keys=ISIS_DATA_HOST_KEY,
        hostname='leaf04',
        groups=['junos'],
        isis_host_data=context.o0503,
        test=True,
        options={}
    )


@given(u'ISIS YAML file should be equal to o0504')
def step_impl(context):
    _compare_isis(
        host_keys=ISIS_DATA_HOST_KEY,
        hostname='leaf04',
        groups=['junos'],
        isis_host_data=context.o0504,
        test=True,
        options={}
    )


@given(u'ISIS o0601 should be equal to o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0701 should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0701 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0702 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS YAML file should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0711 should be equal to o0712')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0711 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0711 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0712 should be equal to o0713')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0712 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'ISIS o0713 should be equal to o0714')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I Finish my ISIS tests and list tests not implemented')
def step_impl(context):
    print("| The following tests are not implemented :")
    for test in context.test_not_implemented:
        print(f"| {test}")
