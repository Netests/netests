#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.plugins.functions.text import print_result
from functions.bgp.juniper.bgp_juniper import (
    _juniper_get_bgp_ssh,
    _juniper_get_bgp_api,
    _juniper_get_bgp_netconf
)
from functions.bgp.cumulus.bgp_cumulus import (
    _cumulus_get_bgp_ssh,
    _cumulus_get_bgp_api,
    _cumulus_get_bgp_netconf
)
from functions.bgp.arista.bgp_arista import (
    _arista_get_bgp_ssh,
    _arista_get_bgp_api,
    _arista_get_bgp_netconf
)
from functions.bgp.nxos.bgp_nxos import (
    _nexus_get_bgp_ssh,
    _nexus_get_bgp_api,
    _nexus_get_bgp_netconf
)
from functions.bgp.ios.bgp_ios import (
    _ios_get_bgp_ssh,
    _ios_get_bgp_api,
    _ios_get_bgp_netconf
)
from functions.bgp.iosxr.bgp_iosxr import (
    _iosxr_get_bgp_ssh,
    _iosxr_get_bgp_api,
    _iosxr_get_bgp_netconf
)
from functions.bgp.extreme_vsp.bgp_extreme_vsp import (
    _extreme_vsp_get_bgp_ssh,
    _extreme_vsp_get_bgp_api,
    _extreme_vsp_get_bgp_netconf
)
from functions.bgp.napalm.bgp_napalm import (
    _generic_bgp_napalm
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    SSH_CONNECTION,
    API_CONNECTION,
    NETCONF_CONNECTION,
    NAPALM_CONNECTION,
    NEXUS_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    ARISTA_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
)
from functions.base_selection import (
    base_selection,
    device_not_compatible_with_napalm
)
from functions.verbose_mode import verbose_mode
from functions.vrf.vrf_get import get_vrf


ERROR_HEADER = "Error import [bgp_gets.py]"
HEADER_GET = "[netests - get_bgp]"

MAPPING_FUNCTION = {
    JUNOS_PLATEFORM_NAME: {
       API_CONNECTION: _juniper_get_bgp_api,
       SSH_CONNECTION: _juniper_get_bgp_ssh,
       NETCONF_CONNECTION: _juniper_get_bgp_netconf,
       NAPALM_CONNECTION: _generic_bgp_napalm
    },
    CUMULUS_PLATEFORM_NAME: {
       API_CONNECTION: _cumulus_get_bgp_api,
       SSH_CONNECTION: _cumulus_get_bgp_ssh,
       NETCONF_CONNECTION: _cumulus_get_bgp_netconf,
       NAPALM_CONNECTION: device_not_compatible_with_napalm
    },
    ARISTA_PLATEFORM_NAME: {
       API_CONNECTION: _arista_get_bgp_api,
       SSH_CONNECTION: _arista_get_bgp_ssh,
       NETCONF_CONNECTION: _arista_get_bgp_netconf,
       NAPALM_CONNECTION: _generic_bgp_napalm
    },
    NEXUS_PLATEFORM_NAME: {
       API_CONNECTION: _nexus_get_bgp_api,
       SSH_CONNECTION: _nexus_get_bgp_ssh,
       NETCONF_CONNECTION: _nexus_get_bgp_netconf,
       NAPALM_CONNECTION: _generic_bgp_napalm
    },
    CISCO_IOS_PLATEFORM_NAME: {
       API_CONNECTION: _ios_get_bgp_api,
       SSH_CONNECTION: _ios_get_bgp_ssh,
       NETCONF_CONNECTION: _ios_get_bgp_netconf,
       NAPALM_CONNECTION: _generic_bgp_napalm
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: _iosxr_get_bgp_api,
        SSH_CONNECTION: _iosxr_get_bgp_ssh,
        NETCONF_CONNECTION: _iosxr_get_bgp_netconf,
        NAPALM_CONNECTION: _generic_bgp_napalm
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: _extreme_vsp_get_bgp_api,
        SSH_CONNECTION: _extreme_vsp_get_bgp_ssh,
        NETCONF_CONNECTION: _extreme_vsp_get_bgp_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    }
}


def get_bgp(nr: Nornir):

    devices = nr.filter()
    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER_GET}] no device selected.")

    get_vrf(nr, save_vrf_name_as_list=True)
    data = devices.run(
        task=generic_bgp_get,
        on_failed=True,
        num_workers=10
    )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        print_result(data)


def generic_bgp_get(task):
    base_selection(
        platform=task.host.platform,
        connection_mode=task.host.data.get("connexion"),
        functions_mapping=MAPPING_FUNCTION
    )(task)
