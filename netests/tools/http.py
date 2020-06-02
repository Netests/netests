#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
from netests.exceptions.netests_exceptions import NetestsHTTPStatusCodeError


def exec_http_call_arista(
    hostname: str,
    port: str,
    username: str,
    password: str,
    command: str,
    secure_api=True,
) -> json:
    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    res = requests.post(
        url=f"{protocol}://{hostname}:{port}/command-api",
        data=json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "runCmds",
                "params": {
                    "format": "json",
                    "timestamps": False,
                    "autoComplete": False,
                    "expandAliases": False,
                    "includeErrorDetail": False,
                    "cmds": [
                        f"{command}"
                    ],
                    "version": 1
                },
                "id": "EapiExplorer-1"
            }
        ),
        headers={'content-type': 'application/json'},
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False
    )

    if res.status_code != 200:
        raise NetestsHTTPStatusCodeError()

    return res.content


def exec_http_call_cumulus(
    hostname: str,
    port: str,
    username: str,
    password: str,
    cumulus_cmd: str,
    secure_api=True,
) -> json:

    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    res = requests.post(
        url=f"{protocol}://{hostname}:{port}/nclu/v1/rpc",
        data=json.dumps(
            {
                "cmd": f"{cumulus_cmd}"
            }
        ),
        headers={'content-type': 'application/json'},
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False
    )

    if res.status_code != 200:
        raise NetestsHTTPStatusCodeError()

    return res.content


def exec_http_call(
    hostname: str,
    port: str,
    username: str,
    password: str,
    endpoint: str,
    secure_api=True,
    header={'content-type': 'application/json'},
    path='/restconf/',
    data={}
) -> json:

    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    res = requests.get(
        url=f"{protocol}://{hostname}:{port}{path}{endpoint}",
        headers=header,
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False,
        data=data
    )

    return res.content


def exec_http_call_juniper(
    hostname: str,
    port: str,
    username: str,
    password: str,
    endpoint,
    secure_api=False,
) -> json:

    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    if isinstance(endpoint, list):
        return juniper_http_post(
            hostname=hostname,
            port=port,
            username=username,
            password=password,
            endpoint=endpoint,
            protocol=protocol,
        )

    res = requests.get(
        url=f"{protocol}://{hostname}:{port}/rpc/{endpoint}",
        headers={'content-type': 'application/xml'},
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False
    )

    return res.content


def juniper_http_post(
    hostname: str,
    port: str,
    username: str,
    password: str,
    endpoint,
    protocol=False,
) -> json:

    res = requests.post(
        url=f"{protocol}://{hostname}:{port}/rpc",
        headers={
            'Content-Type': 'application/xml',
            'Accept': 'application/xml'
        },
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False,
        data="\n".join(endpoint)
    )

    return res.content


def exec_http_nxos(
    hostname: str,
    port: str,
    username: str,
    password: str,
    command: str,
    secure_api=True
) -> json:
    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    res = requests.post(
        url=f"{protocol}://{hostname}:{port}/ins",
        headers={
            'Content-Type': 'application/json',
        },
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False,
        data="""{
            "ins_api": {
                "version": "1.0",
                "type": "cli_show",
                "chunk": "0",
                "sid": "1",
                "input": "%s",
                "output_format": "json"
            }
        }""" % (str(command))
    )

    return res.content


def exec_http_rpc_nxos(
    hostname: str,
    port: str,
    username: str,
    password: str,
    command: str,
    secure_api=True
) -> json:
    if secure_api:
        protocol = "https"
    else:
        protocol = "http"
    res = requests.post(
        url=f"{protocol}://{hostname}:{port}/ins",
        headers={
            'Content-Type': 'application/json-rpc',
        },
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False,
        data="""[
            {
                "jsonrpc": "2.0",
                "method": "cli",
                "params": {
                    "cmd": "%s",
                    "version": 1
                },
                "id": 1
            }
        ]""" % (str(command).replace("\n", ""))
    )

    return res.content


def exec_http_extreme_vsp(
    hostname: str,
    port: str,
    username: str,
    password: str,
    endpoint: str,
    secure_api=True
) -> json:
    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    login = requests.post(
        url=f"{protocol}://{hostname}:{port}/auth/token/",
        headers={
            'Content-Type': 'application/json',
        },
        data="""
            {
                "username": "%s",
                "password": "%s"
            }
        """ % (username, password)
    )
    auth_token = json.loads(login.content).get('token')

    data = requests.get(
        url=f"{protocol}://{hostname}:{port}/rest/restconf/data/{endpoint}",
        headers={
            'X-Auth-Token': auth_token,
        }
    )

    return json.loads(data.content)
