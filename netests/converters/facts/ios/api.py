#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.protocols.facts import Facts
from netests.tools.nc import format_xml_output


def _ios_facts_api_converter(
    hostname: str,
    cmd_output,
    options={}
) -> Facts:

    cmd_output = format_xml_output(cmd_output)

    hostname = NOT_SET
    domain = NOT_SET
    version = NOT_SET
    model = NOT_SET
    serial = NOT_SET
    interfaces_lst = list()
    if (
        isinstance(cmd_output, dict) and
        'Cisco-IOS-XE-native:native' in cmd_output.keys()
    ):
        hostname = cmd_output.get('Cisco-IOS-XE-native:native') \
                             .get('hostname')
        domain = cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('ip') \
                           .get('domain') \
                           .get('name')
        version = cmd_output.get('Cisco-IOS-XE-native:native') \
                            .get('version')
        serial = cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('license') \
                           .get('udi') \
                           .get('sn')
        model = cmd_output.get('Cisco-IOS-XE-native:native') \
                          .get('license') \
                          .get('udi') \
                          .get('pid')
        for t in cmd_output.get('Cisco-IOS-XE-native:native') \
                           .get('interface').keys():
            for i in cmd_output.get('Cisco-IOS-XE-native:native') \
                               .get('interface') \
                               .get(t):
                interfaces_lst.append(f"{t}{i.get('name')}")

    elif (
        isinstance(cmd_output, dict) and
        'native' in cmd_output.keys()
    ):

        hostname = cmd_output.get('native').get('hostname')
        domain = cmd_output.get('native').get('ip').get('domain').get('name')
        version = cmd_output.get('native').get('version')
        serial = cmd_output.get('native').get('license').get('udi').get('sn')
        model = cmd_output.get('native').get('license').get('udi').get('pid')
        for t in cmd_output.get('native').get('interface').keys():
            for i in cmd_output.get('native').get('interface').get(t):
                if isinstance(i, dict):
                    interfaces_lst.append(f"{t}{i.get('name')}")

    return Facts(
        hostname=hostname,
        domain=domain,
        version=version,
        build=NOT_SET,
        serial=serial,
        base_mac=NOT_SET,
        memory=NOT_SET,
        vendor="Cisco",
        model=model,
        interfaces_lst=interfaces_lst,
        options=options
    )
