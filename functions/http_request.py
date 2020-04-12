#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import requests
from const.constants import (
    NOT_SET,
    LEVEL3
)
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from exceptions.netests_exceptions import NetestsHTTPStatusCodeError


def exec_http_call_cumulus(
    hostname:str,
    port: str,
    username:str,
    password:str,
    cumulus_cmd: str
) -> json:
    res = requests.post(
        url=f"https://{hostname}:{port}/nclu/v1/rpc",
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

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL3
    ):
        print(type(res.status_code), res.status_code)
        print(type(res.content), res.content)

    if res.status_code != 200:
        raise NetestsHTTPStatusCodeError()

    return res.content



def exec_http_call(
    hostname: str,
    port: str,
    username: str,
    password: str,
    endpoint: str
) -> json:
    res = requests.get(
        url=f"https://{hostname}:{port}/restconf/{endpoint}",
        headers={'content-type': 'application/json'},
        auth=requests.auth.HTTPBasicAuth(
            f"{username}",
            f"{password}"
        ),
        verify=False
    )

    return res.content
