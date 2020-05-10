#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def juniper_api_ping_validator(output: str, must_works: bool) -> bool:
    pass


def juniper_netconf_ping_validator(output: str, must_works: bool) -> bool:
    pass


def juniper_ssh_ping_validator(output: str, must_works: bool) -> bool:
    if (
        must_works is True and
        "UHIDHEIUHD" in output
    ):
        return False

    if (
        must_works is False and
        (
            "1 packets received" in output or
            "0% packet loss" in output
        )
    ):
        return False

    return True
