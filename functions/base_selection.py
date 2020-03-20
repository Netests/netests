#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def base_selection(platform: str,
                   connection_mode: str,
                   functions_mapping: dict
                   ):
    return functions_mapping.get(platform).get(connection_mode)
