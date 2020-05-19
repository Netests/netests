#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from functions.ospf.juniper.ospf_juniper import (
    _juniper_get_ospf_ssh,
    _juniper_get_ospf_api,
    _juniper_get_ospf_netconf
)
from functions.ospf.cumulus.ospf_cumulus import (
    _cumulus_get_ospf_ssh,
    _cumulus_get_ospf_api,
    _cumulus_get_ospf_netconf
)
from functions.ospf.arista.ospf_arista import (
    _arista_get_ospf_ssh,
    _arista_get_ospf_api,
    _arista_get_ospf_netconf
)
from functions.ospf.nxos.ospf_nxos import (
    _nxos_get_ospf_ssh,
    _nxos_get_ospf_api,
    _nxos_get_ospf_netconf
)
from functions.ospf.ios.ospf_ios import (
    _ios_get_ospf_ssh,
    _ios_get_ospf_api,
    _ios_get_ospf_netconf
)
from functions.ospf.iosxr.ospf_iosxr import (
    _iosxr_get_ospf_ssh,
    _iosxr_get_ospf_api,
    _iosxr_get_ospf_netconf
)
from functions.ospf.extreme_vsp.ospf_extreme_vsp import (
    _extreme_vsp_get_ospf_ssh,
    _extreme_vsp_get_ospf_api,
    _extreme_vsp_get_ospf_netconf
)
from functions.ospf.napalm.ospf_napalm import (
    _generic_ospf_napalm
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


HEADER = "[netests - get_ospf]"

MAPPING_FUNCTION = {
    JUNOS_PLATEFORM_NAME: {
        API_CONNECTION: _juniper_get_ospf_api,
        SSH_CONNECTION: _juniper_get_ospf_ssh,
        NETCONF_CONNECTION: _juniper_get_ospf_netconf,
        NAPALM_CONNECTION: _generic_ospf_napalm
    },
    CUMULUS_PLATEFORM_NAME: {
        API_CONNECTION: _cumulus_get_ospf_api,
        SSH_CONNECTION: _cumulus_get_ospf_ssh,
        NETCONF_CONNECTION: _cumulus_get_ospf_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    },
    ARISTA_PLATEFORM_NAME: {
        API_CONNECTION: _arista_get_ospf_api,
        SSH_CONNECTION: _arista_get_ospf_ssh,
        NETCONF_CONNECTION: _arista_get_ospf_netconf,
        NAPALM_CONNECTION: _generic_ospf_napalm
    },
    NEXUS_PLATEFORM_NAME: {
        API_CONNECTION: _nxos_get_ospf_api,
        SSH_CONNECTION: _nxos_get_ospf_ssh,
        NETCONF_CONNECTION: _nxos_get_ospf_netconf,
        NAPALM_CONNECTION: _generic_ospf_napalm
    },
    CISCO_IOS_PLATEFORM_NAME: {
        API_CONNECTION: _ios_get_ospf_api,
        SSH_CONNECTION: _ios_get_ospf_ssh,
        NETCONF_CONNECTION: _ios_get_ospf_netconf,
        NAPALM_CONNECTION: _generic_ospf_napalm
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: _iosxr_get_ospf_api,
        SSH_CONNECTION: _iosxr_get_ospf_ssh,
        NETCONF_CONNECTION: _iosxr_get_ospf_netconf,
        NAPALM_CONNECTION: _generic_ospf_napalm
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: _extreme_vsp_get_ospf_api,
        SSH_CONNECTION: _extreme_vsp_get_ospf_ssh,
        NETCONF_CONNECTION: _extreme_vsp_get_ospf_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    }
}


def get_ospf(nr: Nornir, options={}):
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

    get_vrf(nr, options)
    data = devices.run(
        task=generic_ospf_get,
        on_failed=True,
        num_workers=10
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        print_result(data)


def generic_ospf_get(task):
    base_selection(
        platform=task.host.platform,
        connection_mode=task.host.data.get("connexion"),
        functions_mapping=MAPPING_FUNCTION
    )(task)
