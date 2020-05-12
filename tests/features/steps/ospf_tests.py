#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functions.ospf.ospf_compare import _compare_ospf
from functions.ospf.arista.ssh.converter import _arista_ospf_ssh_converter
from functions.ospf.cumulus.ssh.converter import _cumulus_ospf_ssh_converter
from functions.global_tools import open_json_file, open_txt_file
from const.constants import FEATURES_SRC_PATH, OSPF_SESSIONS_HOST_KEY
from protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)


@given(u'A network protocols named OSPF defined in protocols/bgp.py')
def step_impl(context):
    context.test_not_implemented = list()


@given(u'I create a OSPF object equals to Arista manually named o0001')
def step_impl(context):
    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    ### VRF - Netests
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="CUSTOMER_NETESTS",
            router_id="153.153.153.153",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )

    ### VRF - default
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ospf_session_lst = ListOSPFSessions(
        ospf_sessions_lst=list()
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            peer_rid="151.151.151.151",
            peer_ip="10.1.2.1",
            local_interface="Ethernet1",
            session_state="FULL"
        )
    )

    ospf_area_lst.ospf_sessions_area_lst.append(
        OSPFSessionsArea(
            area_number="0.0.0.0",
            ospf_sessions=ospf_session_lst
        )
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="default",
            router_id="123.123.123.123",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )

    context.o0001 = OSPF(
        hostname="leaf01",
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )


@given(u'I create a OSPF object from a Arista API output named o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Arista Netconf named o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Arista SSH output named o0004')
def step_impl(context):
    cmd_output = dict()
    cmd_output['default'] = dict()
    cmd_output['default']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_rid.json"
        )
    )
    cmd_output['default']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_neighbors.json"
        )
    )
    cmd_output['CUSTOMER_NETESTS'] = dict()
    cmd_output['CUSTOMER_NETESTS']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_rid_vrf_netests.json"
        )
    )
    cmd_output['CUSTOMER_NETESTS']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_neighbors_vrf_netests.json"
        )
    )
    cmd_output['CUSTOMER_WEJOB'] = dict()
    cmd_output['CUSTOMER_WEJOB']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_rid_vrf_wejob.json"
        )
    )
    cmd_output['CUSTOMER_WEJOB']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/arista/ssh/"
            "arista_ospf_neighbors_vrf_wejob.json"
        )
    )

    context.o0004 = _arista_ospf_ssh_converter(
        hostname="leaf01",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a OSPF object equals to Cumulus manually named o0101')
def step_impl(context):
    ospf_vrf_lst = ListOSPFSessionsVRF(
        ospf_sessions_vrf_lst=list()
    )

    ### VRF - Default
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="default",
            router_id="51.51.51.51",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )
    
    ### VRF - Netests
    ospf_area_lst = ListOSPFSessionsArea(
        ospf_sessions_area_lst=list()
    )

    ospf_session_lst = ListOSPFSessions(
        ospf_sessions_lst=list()
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            peer_rid="53.53.53.53",
            peer_ip="10.1.2.2",
            local_interface="swp1",
            session_state="FULL"
        )
    )

    ospf_session_lst.ospf_sessions_lst.append(
        OSPFSession(
            peer_rid="62.62.62.62",
            peer_ip="10.1.20.2",
            local_interface="swp2",
            session_state="FULL"
        )
    )

    ospf_area_lst.ospf_sessions_area_lst.append(
        OSPFSessionsArea(
            area_number="0.0.0.0",
            ospf_sessions=ospf_session_lst
        )
    )

    ospf_vrf_lst.ospf_sessions_vrf_lst.append(
        OSPFSessionsVRF(
            vrf_name="NETESTS_VRF",
            router_id="151.151.151.151",
            ospf_sessions_area_lst=ospf_area_lst
        )
    )

    context.o0101 = OSPF(
        hostname="leaf01",
        ospf_sessions_vrf_lst=ospf_vrf_lst
    )


@given(u'I create a OSPF object from a Cumulus API output named o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Cumulus Netconf named o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Cumulus SSH output named o0104')
def step_impl(context):
    cmd_output = dict()
    cmd_output['default'] = dict()
    cmd_output['default']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_rid.json"
        )
    )
    cmd_output['default']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_neighbors.json"
        )
    )
    cmd_output['NETESTS_VRF'] = dict()
    cmd_output['NETESTS_VRF']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_rid_vrf_netests.json"
        )
    )
    cmd_output['NETESTS_VRF']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_neighbors_vrf_netests.json"
        )
    )
    cmd_output['mgmt'] = dict()
    cmd_output['mgmt']['rid'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_rid_vrf_mgmt.json"
        )
    )
    cmd_output['mgmt']['data'] = open_txt_file(
        path=(
            f"{FEATURES_SRC_PATH}outputs/ospf/cumulus/ssh/"
            "cumulus_ospf_neighbors_vrf_mgmt.json"
        )
    )

    context.o0104 = _cumulus_ospf_ssh_converter(
        hostname="leaf01",
        cmd_output=cmd_output,
        options={}
    )


@given(u'I create a OSPF object equals to Extreme VSP manually named o0201')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Extreme VSP API output named o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Extreme VSP Netconf output named o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Extreme VSP SSH output named o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals to IOS manually named o0301')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS API output named o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS Netconf named o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS SSH named o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals to IOS-XR manually named o0401')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS-XR API output named o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS-XR Netconf output named o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS-XR SSH output named o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals IOS-XR multi manually output named o0405')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a IOS-XR multi Netconf output named o0406')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals to Juniper manually named o0501')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Juniper API output named o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Juniper Netconf output named o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a Juniper SSH output named o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals to NAPALM manually named o0601')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a NAPALM output named o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object equals to NXOS manually named o0701')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a NXOS API output named o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a NXOS Netconf output named o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I create a OSPF object from a NXOS SSH output named o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0001 should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0001 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0001 should be equal to o0004')
def step_impl(context):
    assert context.o0001 == context.o0004


@given(u'OSPF o0002 should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0002 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0003 should be equal to o0004')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0002')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0003')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0004')
def step_impl(context):
    _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname='leaf03',
        groups=['eos'],
        ospf_host_data=context.o0004,
        test=True,
        options={}
    )


@given(u'OSPF o0101 should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0101 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0101 should be equal to o0104')
def step_impl(context):
    assert context.o0101 == context.o0104


@given(u'OSPF o0102 should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0102 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0103 should be equal to o0104')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0102')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0103')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0104')
def step_impl(context):
    _compare_ospf(
        host_keys=OSPF_SESSIONS_HOST_KEY,
        hostname='leaf01',
        groups=['linux'],
        ospf_host_data=context.o0104,
        test=True,
        options={}
    )


@given(u'OSPF o0201 should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0201 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0201 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0202 should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0202 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0203 should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0202')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0203')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0204')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0301 should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0301 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0301 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0302 should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0302 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0303 should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0302')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0303')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0304')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0401 should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0401 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0401 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0402 should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0402 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0403 should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0402')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0403')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0404')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0501 should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0501 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0501 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0502 should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0502 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0503 should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0502')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0503')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0504')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0601 should be equal to o0602')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0701 should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0701 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0701 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0702 should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0702 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF o0703 should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0702')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0703')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'OSPF YAML file should be equal to o0704')
def step_impl(context):
    context.scenario.tags.append("own_skipped")


@given(u'I Finish my OSPF tests and list tests not implemented')
def step_impl(context):
    context.scenario.tags.append("own_skipped")
