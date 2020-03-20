#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from exceptions.netests_exceptions import (
    NetestsDeviceNotCompatibleWithNapalm
)


def base_selection(platform: str,
                   connection_mode: str,
                   functions_mapping: dict
                   ):
    return functions_mapping.get(platform).get(connection_mode)


def device_not_compatible_with_napalm(task):
    raise NetestsDeviceNotCompatibleWithNapalm(
        f"Device {task.host.platform} is not compatible with NAPALM...."
    )
