#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from protocols.vrf import (
    ListVRF
)


def _juniper_vrf_api_converter(hostname: str, cmd_outputs: list) -> ListVRF:
    print("_juniper_vrf_api_converter")
