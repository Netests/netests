#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from jnpr.junos import Device
from xml.etree import ElementTree
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL5, PING_DATA_HOST_KEY
from exceptions.netests_exceptions import NetestsErrorWithPingExecution
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_ping_netconf_exec(task, options={}):
    error_lst = list()
    with Device(
        host=task.host.hostname,
        port=task.host.port,
        user=task.host.username,
        passwd=task.host.password,
    ) as m:
        for ping_line in task.host[PING_DATA_HOST_KEY].ping_lst:
            o = m.rpc.ping(
                count="1",
                wait="1",
                host=ping_line.ip_address,
                routing_instance=ping_line.vrf
            )

            o = format_xml_output(o)

            if verbose_mode(
                user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
                needed_value=LEVEL5
            ):
                printline()
                PP.pprint(o)
                PP.pprint(ping_line.to_json())

            if 'ping-results' in o.keys():
                if (
                    'ping-failure' in o.get('ping-results') and
                    ping_line.works is True
                ):
                    error_lst.append(ping_line)
            
                if (
                    'ping-success' in o.get('ping-results') and
                    ping_line.works is False
                ):
                    error_lst.append(ping_line)
            else:
                    error_lst.append(ping_line)

    if len(error_lst) > 0:
        raise NetestsErrorWithPingExecution(error_lst)
