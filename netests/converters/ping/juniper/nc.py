#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests import log
from jnpr.junos import Device
from nornir.core.task import Result
from netests.tools.nc import format_xml_output
from netests.constants import PING_DATA_HOST_KEY
from netests.converters.ping.ping_validator import _raise_exception_on_ping_cmd


def _juniper_ping_nc_exec(task):
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:
        result = True
        for p in task.host[PING_DATA_HOST_KEY].ping_lst:
            o = m.rpc.ping(
                count="1",
                wait="1",
                host=p.ip_address,
                routing_instance=p.vrf
            )

            o = format_xml_output(o)

            log.debug(
                "\n"
                "Execute the following ping command on Juniper Netconf\n"
                f"ping=count=1,wait=1,host=p.ip_address,routing_instance=p.vrf"
                "From the following PING object :\n"
                f"{p.to_json()}"
                "Result is :\n"
                f"{o}"
            )

            if 'ping-results' in o.keys():
                r = _raise_exception_on_ping_cmd(
                    output=o,
                    hostname=task.host.name,
                    platform=task.host.platform,
                    connexion=task.host.get('connexion'),
                    ping_line=p,
                    must_work=p.works
                )

                if r is False:
                    result = False

    return Result(host=task.host, result=result)
