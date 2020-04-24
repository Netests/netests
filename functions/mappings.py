#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from const.constants import (
    BGP_STATE_UP_LIST,
    BGP_STATE_BRIEF_UP,
    BGP_STATE_BRIEF_DOWN,
    BGP_UPTIME_FORMAT_MS
)


def get_bgp_state_brief(state: str) -> str:
    if state in BGP_STATE_UP_LIST:
        return BGP_STATE_BRIEF_UP
    else:
        return BGP_STATE_BRIEF_DOWN


def get_bgp_peer_uptime(value: str, format: str) -> str:
    if format == BGP_UPTIME_FORMAT_MS:
        return value
