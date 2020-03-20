#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import os
import json
import yaml
import time
from const.constants import (
    NOT_SET,
    REPORT_FOLDER,
    BGP_WORKS_KEY,
    BGP_SESSIONS_HOST_KEY
)

ERROR_HEADER = "Error import [bgp_reports.py]"
HEADER_GET = "[netests - bgp_reports]"


def create_reports(nr, bgp_data: json):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    today = time.strftime("%Y-%m-%d_%H:%M")

    if not os.path.exists(REPORT_FOLDER):
        os.makedirs(REPORT_FOLDER)

    if not os.path.exists(f"{REPORT_FOLDER}{today}/"):
        os.makedirs(f"{REPORT_FOLDER}{today}/")

    data = devices.run(
        task=_create,
        bgp_data=bgp_data,
        today=today,
        on_failed=True,
        num_workers=10
    )

    return not data.failed


def _create(task, bgp_data: json, today: str):

    data_yaml = dict()
    data_yaml[task.host.name] = dict()

    data_yaml[task.host.name]["works"] = task.host.get(BGP_WORKS_KEY, NOT_SET)

    data_yaml[task.host.name]["vrfs"] = dict()

    for vrf_name, facts in bgp_data.get(task.host.name).items():

        data_yaml[task.host.name]["vrfs"][vrf_name] = dict()

        data_yaml[task.host.name]["vrfs"][vrf_name]["as_number"] = dict()
        data_yaml[task.host.name]["vrfs"][vrf_name]["as_number"][
            "should_be"
        ] = facts.get("asn", NOT_SET)

        for bgp_session_vrf in task.host.get(
            BGP_SESSIONS_HOST_KEY
        ).bgp_sessions_vrf_lst.bgp_sessions_vrf:
            if str(bgp_session_vrf.vrf_name) == str(vrf_name):
                data_yaml[task.host.name]["vrfs"][vrf_name]["as_number"][
                    "current_is"
                ] = str(bgp_session_vrf.as_number)

        data_yaml[task.host.name]["vrfs"][vrf_name]["router_id"] = dict()
        data_yaml[task.host.name]["vrfs"][vrf_name]["router_id"][
            "should_be"
        ] = facts.get("router_id", NOT_SET)
        for bgp_session_vrf in task.host.get(
            BGP_SESSIONS_HOST_KEY
        ).bgp_sessions_vrf_lst.bgp_sessions_vrf:
            if str(bgp_session_vrf.vrf_name) == str(vrf_name):
                data_yaml[task.host.name]["vrfs"][vrf_name]["router_id"][
                    "current_is"
                ] = str(bgp_session_vrf.router_id)

        data_yaml.get(task.host.name).get("vrfs") \
            .get(vrf_name)["neighbors"] = list()

        for bgp_session_vrf in task.host.get(
            BGP_SESSIONS_HOST_KEY
        ).bgp_sessions_vrf_lst.bgp_sessions_vrf:
            if str(bgp_session_vrf.vrf_name) == str(vrf_name):
                for neighbor in bgp_session_vrf.bgp_sessions.bgp_sessions:
                    tmp_dict = dict()
                    tmp_dict["src_hostname"] = neighbor.src_hostname
                    tmp_dict["peer_ip"] = neighbor.peer_ip
                    tmp_dict["remote_as"] = neighbor.remote_as
                    tmp_dict["peer_hostname"] = neighbor.peer_hostname
                    tmp_dict["state_brief"] = neighbor.state_brief
                    tmp_dict["session_state"] = neighbor.session_state
                    tmp_dict["state_time"] = neighbor.state_time
                    tmp_dict["prefix_received"] = neighbor.prefix_received

                    data_yaml.get(task.host.name).get("vrfs").get(vrf_name) \
                        .get("neighbors").append(tmp_dict)

    with open(f"{REPORT_FOLDER}{today}/{task.host.name}.yml", "w+") as outfile:
        yaml.dump(data_yaml, outfile, default_flow_style=False)
