#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def nxos_generic_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "address is not permitted" in output or
            "No route to host" in output or
            "100.00% packet loss" in output or
            "0 packets received" in output or
            "ping: bad context" in output or
            "Invalid host/interface" in output
        )
    ):
        return False

    if (
        must_works is False and
        (
            "1 packets received" in output or
            # DONT REMOVE THE SPACE BEFORE THE '0' !!!
            " 0.00% packet loss" in output or
            "round-trip min/avg/max" in output
        )
    ):
        return False

    return True


def nxos_api_ping_validator(output: str, must_works: bool) -> bool:
    return nxos_generic_ping_validator(output, must_works)


def nxos_netconf_ping_validator(output: str, must_works: bool) -> bool:
    return False


def nxos_ssh_ping_validator(output: str, must_works: bool) -> bool:
    return nxos_generic_ping_validator(output, must_works)
