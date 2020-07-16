#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from nornir.core.task import Task
from netests import log
from netests.tools.file import open_file
from netests.select_vars import select_host_vars
from netests.protocols.isis import (
    ISISAdjacency,
    ListISISAdjacency,
    ISISAdjacencyVRF,
    ListISISAdjacencyVRF,
    ISIS
)
from netests.comparators.log_compare import log_compare, log_no_yaml_data
from netests.constants import NOT_SET, ISIS_DATA_HOST_KEY, ISIS_WORKS_KEY
from netests.exceptions.netests_exceptions import (
    NetestsOverideTruthVarsKeyUnsupported
)


def _compare_transit_isis(task, options={}):

    task.host[ISIS_WORKS_KEY] = _compare_isis(
        host_keys=task.host.keys(),
        hostname=task.host.name,
        groups=task.host.groups,
        isis_host_data=task.host.get(ISIS_DATA_HOST_KEY, None),
        test=False,
        options=options,
        task=task
    )

    return task.host[ISIS_WORKS_KEY]


def _compare_isis(
    host_keys,
    hostname: str,
    groups: list,
    isis_host_data: ISIS,
    test=False,
    options={},
    task=Task
) -> bool:
    if (
        'own_vars' in options.keys() and
        options.get('own_vars') is not None and
        'enable' in options.get('own_vars').keys() and
        options.get('own_vars').get('enable') is True
    ):
        raise NetestsOverideTruthVarsKeyUnsupported()
    else:
        if test:
            isis_yaml_data = open_file(
                path="tests/features/src/isis_tests.yml"
            ).get(hostname)
        else:
            isis_yaml_data = select_host_vars(
                hostname=hostname,
                groups=groups,
                protocol="isis"
            )

        verity_isis = ISIS(
            isis_vrf_lst=list()
        )

        log.debug(
            "ISIS_DATA_HOST_KEY in host_keys="
            f"{ISIS_DATA_HOST_KEY in host_keys}\n"
            "isis_yaml_data is not None="
            f"{isis_yaml_data is not None}"
        )
        if (
            ISIS_DATA_HOST_KEY in host_keys and
            isis_yaml_data is not None
        ):
            isis_vrf_lst = ListISISAdjacencyVRF(
                isis_vrf_lst=list()
            )

            for isis_vrf in isis_yaml_data:
                isis_adj_lst = ListISISAdjacency(
                    isis_adj_lst=list()
                )

                for i in isis_vrf.get('adjacencies', list()):
                    isis_adj_lst.isis_adj_lst.append(
                        ISISAdjacency(
                            session_state=i.get('session_state', NOT_SET),
                            level_type=i.get('level_type', NOT_SET),
                            circuit_type=i.get('circuit_type', NOT_SET),
                            local_interface_name=i.get(
                                'local_interface_name', NOT_SET
                            ),
                            neighbor_sys_name=i.get(
                                'neighbor_sys_name', NOT_SET
                            ),
                            neighbor_ip_addr=i.get(
                                'neighbor_ip_addr', NOT_SET
                            ),
                            snap=i.get('snap', NOT_SET)
                        )
                    )

                isis_vrf_lst.isis_vrf_lst.append(
                    ISISAdjacencyVRF(
                        router_id=isis_vrf.get('router_id', NOT_SET),
                        system_id=isis_vrf.get('system_id', NOT_SET),
                        area_id=isis_vrf.get('area_id', NOT_SET),
                        vrf_name=isis_vrf.get('vrf_name', NOT_SET),
                        adjacencies=isis_adj_lst,
                    )
                )

            verity_isis = ISIS(
                isis_vrf_lst=isis_vrf_lst
            )

            log_compare(verity_isis, isis_host_data, hostname, groups)
            return verity_isis == isis_host_data

        else:
            log_no_yaml_data(
                "isis",
                ISIS_DATA_HOST_KEY,
                "ISIS_DATA_HOST_KEY",
                hostname,
                groups
            )
            return True
