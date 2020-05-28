#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.exceptions.netests_exceptions import NetestsOverideTruthVarsKeyUnsupported
from netests.protocols.ospf import (
    OSPFSession,
    ListOSPFSessions,
    OSPFSessionsArea,
    ListOSPFSessionsArea,
    OSPFSessionsVRF,
    ListOSPFSessionsVRF,
    OSPF
)
from netests.constants import NOT_SET, OSPF_WORKS_KEY, OSPF_SESSIONS_HOST_KEY


def _compare_transit_ospf(task, options={}):
    task.host[OSPF_WORKS_KEY] = _compare_ospf(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        ospf_host_data=task.host.get(OSPF_SESSIONS_HOST_KEY, None),
        test=False,
        options=options,
        task=task
    )
    return task.host[OSPF_WORKS_KEY]


def _compare_ospf(
    host_keys,
    hostname,
    groups,
    ospf_host_data: OSPF,
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
            ospf_yaml_data = open_file(
                path="tests/features/src/ospf_tests.yml"
            ).get(hostname)
        else:
            ospf_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="ospf"
            )

        ospf_sessions_vrf_lst = ListOSPFSessionsVRF(
            list()
        )

        log.debug(
            "OSPF_SESSIONS_HOST_KEY in host_keys="
            f"{OSPF_SESSIONS_HOST_KEY in host_keys}\n"
            "ospf_yaml_data is not None="
            f"{ospf_yaml_data is not None}"
        )
        if (
            OSPF_SESSIONS_HOST_KEY in host_keys and
            ospf_yaml_data is not None
        ):
            for v, f in ospf_yaml_data.items():
                ospf_sessions_vrf = OSPFSessionsVRF(
                    router_id=f.get('router_id', NOT_SET),
                    vrf_name=v,
                    ospf_sessions_area_lst=ListOSPFSessionsArea(list())
                )

                for a, s in f.get('area_id', NOT_SET).items():
                    ospf_a = OSPFSessionsArea(
                        area_number=a,
                        ospf_sessions=ListOSPFSessions(list())
                    )

                    for n in s:
                        if isinstance(n, dict):
                            ospf_a.ospf_sessions.ospf_sessions_lst.append(
                                OSPFSession(
                                    peer_rid=n.get('peer_rid', NOT_SET),
                                    peer_hostname=n.get('peer_name', NOT_SET),
                                    session_state=n.get('state', NOT_SET),
                                    local_interface=n.get(
                                        'local_interface', NOT_SET),
                                    peer_ip=n.get('peer_ip', NOT_SET)
                                )
                            )

                    ospf_sessions_vrf.ospf_sessions_area_lst \
                        .ospf_sessions_area_lst \
                        .append(ospf_a)

                ospf_sessions_vrf_lst.ospf_sessions_vrf_lst.append(
                    ospf_sessions_vrf
                )

            verity_ospf = OSPF(
                hostname=hostname,
                ospf_sessions_vrf_lst=ospf_sessions_vrf_lst
            )

            log_compare(verity_ospf, ospf_host_data, hostname, groups)
            return verity_ospf == ospf_host_data

        else:
            log_no_yaml_data(
                "ospf",
                OSPF_SESSIONS_HOST_KEY,
                "OSPF_SESSIONS_HOST_KEY",
                hostname,
                groups
            )
            return True

