#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def ios_api_ping_validator(output: str, must_works: bool) -> bool:
    return False


def ios_netconf_ping_validator(output: str, must_works: bool) -> bool:
    return False


def ios_ssh_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "Unrecognized host or address" in output or
            "Success rate is 0 percent" in output or
            "Invalid input detected at" in output or
            "Unable to find vrf" in output or
            "does not have a usable source address" in output
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
