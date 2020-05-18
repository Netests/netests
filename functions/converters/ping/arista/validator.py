#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def arista_generic_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "Network is unreachable" in output or
            "failure in name resolution" in output or
            "100% packet loss" in output or
            "0 received" in output or
            "Invalid input - VRF" in output
        )
    ):
        return False

    if (
        must_works is False and
        (
            "rtt min/avg/max/mdev" in output or
            "1 received" in output or
            # DONT REMOVE THE SPACE BEFORE THE '0' !!!
            " 0% packet loss" in output
        )
    ):
        return False

    return True


def arista_api_ping_validator(output: str, must_works: bool) -> bool:
    return arista_generic_ping_validator(output, must_works)


def arista_netconf_ping_validator(output: str, must_works: bool) -> bool:
    return False


def arista_ssh_ping_validator(output: str, must_works: bool) -> bool:
    return arista_generic_ping_validator(output, must_works)
