#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from functions.lldp.arista.lldp_arista import (
    _arista_get_lldp_ssh,
    _arista_get_lldp_api,
    _arista_get_lldp_netconf
)
from functions.lldp.cumulus.lldp_cumulus import (
    _cumulus_get_lldp_ssh,
    _cumulus_get_lldp_api,
    _cumulus_get_lldp_netconf
)
from functions.lldp.extreme_vsp.lldp_extreme_vsp import (
    _extreme_vsp_get_lldp_ssh,
    _extreme_vsp_get_lldp_api,
    _extreme_vsp_get_lldp_netconf
)
from functions.lldp.ios.lldp_ios import (
    _ios_get_lldp_ssh,
    _ios_get_lldp_api,
    _ios_get_lldp_netconf
)
from functions.lldp.iosxr.lldp_iosxr import (
    _iosxr_get_lldp_ssh,
    _iosxr_get_lldp_api,
    _iosxr_get_lldp_netconf
)
from functions.lldp.juniper.lldp_juniper import (
    _juniper_get_lldp_ssh,
    _juniper_get_lldp_api,
    _juniper_get_lldp_netconf
)
from functions.lldp.napalm.lldp_napalm import (
    _generic_lldp_napalm
)
from functions.lldp.nxos.lldp_nxos import (
    _nxos_get_lldp_ssh,
    _nxos_get_lldp_api,
    _nxos_get_lldp_netconf
)

from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL4,
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


HEADER = "[netests - get_lldp]"

MAPPING_FUNCTION = {
    JUNOS_PLATEFORM_NAME: {
        API_CONNECTION: _juniper_get_lldp_api,
        SSH_CONNECTION: _juniper_get_lldp_ssh,
        NETCONF_CONNECTION: _juniper_get_lldp_netconf,
        NAPALM_CONNECTION: _generic_lldp_napalm
    },
    CUMULUS_PLATEFORM_NAME: {
        API_CONNECTION: _cumulus_get_lldp_api,
        SSH_CONNECTION: _cumulus_get_lldp_ssh,
        NETCONF_CONNECTION: _cumulus_get_lldp_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    },
    ARISTA_PLATEFORM_NAME: {
        API_CONNECTION: _arista_get_lldp_api,
        SSH_CONNECTION: _arista_get_lldp_ssh,
        NETCONF_CONNECTION: _arista_get_lldp_netconf,
        NAPALM_CONNECTION: _generic_lldp_napalm
    },
    NEXUS_PLATEFORM_NAME: {
        API_CONNECTION: _nxos_get_lldp_api,
        SSH_CONNECTION: _nxos_get_lldp_ssh,
        NETCONF_CONNECTION: _nxos_get_lldp_netconf,
        NAPALM_CONNECTION: _generic_lldp_napalm
    },
    CISCO_IOS_PLATEFORM_NAME: {
        API_CONNECTION: _ios_get_lldp_api,
        SSH_CONNECTION: _ios_get_lldp_ssh,
        NETCONF_CONNECTION: _ios_get_lldp_netconf,
        NAPALM_CONNECTION: _generic_lldp_napalm
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: _iosxr_get_lldp_api,
        SSH_CONNECTION: _iosxr_get_lldp_ssh,
        NETCONF_CONNECTION: _iosxr_get_lldp_netconf,
        NAPALM_CONNECTION: _generic_lldp_napalm
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: _extreme_vsp_get_lldp_api,
        SSH_CONNECTION: _extreme_vsp_get_lldp_ssh,
        NETCONF_CONNECTION: _extreme_vsp_get_lldp_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    }
}


def get_lldp(nr: Nornir, options={}):
    if (
        'from_cli' in options.keys() and
        options.get('from_cli') is not None and
        options.get("from_cli") is True and
        isinstance(options.get("from_cli"), bool)
    ):
        devices = nr.filter(F(groups__contains="netests"))
        os.environ["NETESTS_VERBOSE"] = LEVEL1
    else:
        devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        print(f"[{HEADER}] no device selected.")

    data = devices.run(
        task=generic_lldp_get,
        on_failed=True,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        print_result(data)


def generic_lldp_get(task):
    base_selection(
        platform=task.host.platform,
        connection_mode=task.host.data.get("connexion"),
        functions_mapping=MAPPING_FUNCTION
    )(task)
