#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.protocols.bgp import BGP


def _iosxr_bgp_api_converter(hostname: str, cmd_outputs: list) -> BGP:
    print("_iosxr_bgp_api_converter")
