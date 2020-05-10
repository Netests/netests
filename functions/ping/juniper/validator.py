#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def juniper_generic_ping_validator(output: str, must_works: bool) -> bool:
    if 'ping-failure' in output.get('ping-results') and must_works is True:
        return False

    if 'ping-success' in output.get('ping-results') and must_works is False:
        return False

    return True


def juniper_api_ping_validator(output: str, must_works: bool) -> bool:
    return juniper_generic_ping_validator(output, must_works)


def juniper_netconf_ping_validator(output: str, must_works: bool) -> bool:
    return juniper_generic_ping_validator(output, must_works)


def juniper_ssh_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "100% packet loss" in output or
            "0 packets received" in output or
            "assign requested address" in output or
            "invalid routing instance" in output or
            "Host name lookup failure" in output or
            "No route to host" in output
        )
    ):
        return False

    if (
        must_works is False and
        (
            "1 packets received" in output or
            " 0% packet loss" in output or
            "round-trip min/avg/max/stddev" in output
        )
    ):
        return False

    return True
