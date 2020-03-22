#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocols.bgp import (
    BGP
)


def _iosxr_bgp_ssh_converter(hostname: str, cmd_outputs: list) -> BGP:
    print("_iosxr_bgp_ssh_converter")
