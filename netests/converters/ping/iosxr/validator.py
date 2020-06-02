#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def iosxr_api_ping_validator(output: str, must_works: bool) -> bool:
    return False


def iosxr_netconf_ping_validator(output: str, must_works: bool) -> bool:
    if (
        isinstance(output, dict) and
        'rpc-reply' in output.keys() and
        'ping-response' in output.get('rpc-reply').keys() and
        'ipv4' in output.get('rpc-reply').get('ping-response').keys()
    ):
        if (
            (
                output.get('rpc-reply')
                      .get('ping-response')
                      .get('ipv4')
                      .get('success-rate') == '100' and
                must_works is False
            ) or
            (
                output.get('rpc-reply')
                      .get('ping-response')
                      .get('ipv4')
                      .get('success-rate') == '0' and
                must_works is True
            )
        ):
            return False

    if (
        isinstance(output, dict) and
        'rpc-reply' in output.keys() and
        'rpc-error' in output.get('rpc-reply').keys() and
        must_works is True
    ):
        return False

    return True


def iosxr_ssh_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "Bad hostname or protocol" in output or
            "Success rate is 0 percent" in output or
            "Invalid vrf table name" in output
        )
    ):
        return False

    if (
        must_works is False and
        (
            "Success rate is 100 percent" in output or
            "round-trip min/avg/max" in output
        )
    ):
        return False

    return True
