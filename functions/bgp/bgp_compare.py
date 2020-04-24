#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from const.constants import (
    NOT_SET,
    BGP_SESSIONS_HOST_KEY,
    BGP_STATE_BRIEF_UP,
    BGP_WORKS_KEY
)
from protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.global_tools import open_file
from functions.select_vars import select_host_vars
from exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported


HEADER = "[netests - compare_bgp]"


def compare_bgp(nr, options={}) -> bool:

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=_compare_transit_bgp,
        options=options,
        on_failed=True,
        num_workers=10
    )

    return_value = True

    for value in data.values():
        if value.result is False:
            print(
                f"{HEADER} Task '_compare' has failed for "
                f"{value.host} (value.result={value.result})."
            )
            return_value = False

    return (not data.failed and return_value)


def _compare_transit_bgp(task, options={}):

    task.host[BGP_WORKS_KEY] = _compare_bgp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        bgp_host_data=task.host[BGP_SESSIONS_HOST_KEY],
        test=False,
        options=options,
        task=task
    )

    return task.host[BGP_WORKS_KEY]


def _compare_bgp(
    host_keys,
    hostname,
    groups,
    bgp_host_data: BGP,
    test=False,
    options={},
    task=Task
):
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            bgp_yaml_data = open_file(
                path="tests/features/src/bgp_tests.yml"
            ).get(hostname)
        else:
            bgp_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="bgp"
            )

        bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

        if BGP_SESSIONS_HOST_KEY in host_keys:
            for vrf_name, facts in bgp_yaml_data.items():
                bgp_sessions_lst = ListBGPSessions(list())
                for neighbor in facts.get('neighbors', NOT_SET):
                    bgp_session = BGPSession(
                        src_hostname=hostname,
                        peer_ip=neighbor.get('peer_ip', NOT_SET),
                        peer_hostname=neighbor.get('peer_hostname', NOT_SET),
                        remote_as=neighbor.get('remote_as', NOT_SET),
                        state_brief=neighbor.get('state', BGP_STATE_BRIEF_UP),
                    )
                    bgp_sessions_lst.bgp_sessions.append(bgp_session)

                bgp_session_vrf = BGPSessionsVRF(
                    vrf_name=vrf_name,
                    as_number=facts.get('asn', NOT_SET),
                    router_id=facts.get('router_id', NOT_SET),
                    bgp_sessions=bgp_sessions_lst
                )
                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

            verity_bgp = BGP(
                hostname=hostname,
                bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
            )

            return verity_bgp == bgp_host_data

        else:
            print(f"Key {BGP_SESSIONS_HOST_KEY} is missing for {hostname}")
            return False
