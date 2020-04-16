#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from const.constants import (
    NOT_SET,
    LEVEL3
)
from functions.verbose_mode import verbose_mode
from exceptions.netests_exceptions import NetestsHTTPStatusCodeError


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
) -> json:

    if secure_api:
        protocol = "https"
    else:
        protocol = "http"

    res = requests.get(
        url=f"{protocol}://{hostname}:{port}/restconf/{endpoint}",
        headers={'content-type': 'application/json'},
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False
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
            'Content-Typ': 'application/xml',
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
