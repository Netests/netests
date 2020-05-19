#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def extreme_vsp_api_ping_validator(output: str, must_works: bool) -> bool:
    return False


def extreme_vsp_netconf_ping_validator(output: str, must_works: bool) -> bool:
    return False


def extreme_vsp_ssh_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        (
            "The VRF Name entered does not correspond" in output or
            "no answer from" in output or
            "Invalid host name format or IP address" in output
        )
    ):
        return False

    if (
        must_works is False and
        (
            "is alive" in output
        )
    ):
        return False

    return True
