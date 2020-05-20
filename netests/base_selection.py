#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import PLATFORM_SUPPORTED, CONNEXION_MODE

from netests.exceptions.netests_exceptions import (
    NetestsDeviceNotCompatibleWithNapalm
)


HEADER = "[netests - base_selection]"


def base_selection(platform: str,
                   connection_mode: str,
                   functions_mapping: dict
                   ):
    return functions_mapping.get(platform).get(connection_mode)


def device_not_compatible_with_napalm(task):
    raise NetestsDeviceNotCompatibleWithNapalm(
        f"Device {task.host.platform} is not compatible with NAPALM...."
    )


def host_vars_ok(hostname: str, platform: str, connection_mode: str) -> bool:
    if (
        platform in PLATFORM_SUPPORTED and
        connection_mode in CONNEXION_MODE
    ):
        return True
    else:
        print(
            f"{HEADER} ({hostname}) Connexion type not allowed  \n"
            f"{HEADER} Connexion must be one of the followings: \n"
            f"{HEADER} {CONNEXION_MODE}"
        )
        return False
