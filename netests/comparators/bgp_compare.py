#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.constants import NOT_SET, BGP_SESSIONS_HOST_KEY, BGP_WORKS_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)
from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)


def _compare_transit_bgp(task, options={}):
    task.host[BGP_WORKS_KEY] = _compare_bgp(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        bgp_host_data=task.host.get(BGP_SESSIONS_HOST_KEY, None),
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

        log.debug(
            "BGP_SESSIONS_HOST_KEY in host_keys="
            f"{BGP_SESSIONS_HOST_KEY in host_keys}\n"
            "bgp_yaml_data is not None="
            f"{bgp_yaml_data is not None}"
        )
        if (
            BGP_SESSIONS_HOST_KEY in host_keys and
            bgp_yaml_data is not None
        ):
            for vrf_name, facts in bgp_yaml_data.items():
                bgp_sessions_lst = ListBGPSessions(
                    list()
                )
                for n in facts.get('neighbors', []):
                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=n.get('peer_ip', NOT_SET),
                            peer_hostname=n.get('peer_hostname', NOT_SET),
                            remote_as=n.get('remote_as', NOT_SET),
                            state_brief=n.get('state_brief', NOT_SET),
                            session_state=n.get('session_state', NOT_SET),
                            state_time=n.get('state_time', NOT_SET),
                            prefix_received=n.get('prefix_received', NOT_SET),
                        )
                    )

                bgp_session_vrf = BGPSessionsVRF(
                    vrf_name=vrf_name,
                    as_number=facts.get('as_number', NOT_SET),
                    router_id=facts.get('router_id', NOT_SET),
                    bgp_sessions=bgp_sessions_lst
                )
                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(bgp_session_vrf)

            verity_bgp = BGP(
                hostname=hostname,
                bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
            )

            log_compare(verity_bgp, bgp_host_data, hostname, groups)
            return verity_bgp == bgp_host_data

        else:
            log_no_yaml_data(
                "bgp",
                BGP_SESSIONS_HOST_KEY,
                "BGP_SESSIONS_HOST_KEY",
                hostname,
                groups
            )
            return True
