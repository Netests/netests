#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.plugins.functions.text import print_result
from functions.bond.bond_get import get_bond
from functions.vlan.arista.vlan_arista import (
    _arista_get_vlan_api,
    _arista_get_vlan_netconf,
    _arista_get_vlan_ssh
)
from functions.vlan.cumulus.vlan_cumulus import (
    _cumulus_get_vlan_api,
    _cumulus_get_vlan_netconf,
    _cumulus_get_vlan_ssh
)
from functions.vlan.extreme_vsp.vlan_extreme_vsp import (
    _extreme_vsp_get_vlan_api,
    _extreme_vsp_get_vlan_netconf,
    _extreme_vsp_get_vlan_ssh
) 
from functions.vlan.ios.vlan_ios import (
    _ios_get_vlan_api,
    _ios_get_vlan_netconf,
    _ios_get_vlan_ssh
)
from functions.vlan.iosxr.vlan_iosxr import (
    _iosxr_get_vlan_api,
    _iosxr_get_vlan_netconf,
    _iosxr_get_vlan_ssh
)
from functions.vlan.juniper.vlan_juniper import (
    _juniper_get_vlan_api,
    _juniper_get_vlan_netconf,
    _juniper_get_vlan_ssh
)
from functions.vlan.napalm.vlan_napalm import (
    _generic_vlan_napalm
)
from functions.vlan.nxos.vlan_nxos import (
    _nxos_get_vlan_api,
    _nxos_get_vlan_netconf,
    _nxos_get_vlan_ssh
)
from functions.base_selection import (
    base_selection,
    device_not_compatible_with_napalm
)
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL2,
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


HEADER = "[netests - get_vlan]"
MAPPING_FUNCTION = {
    JUNOS_PLATEFORM_NAME: {
        API_CONNECTION: _juniper_get_vlan_api,
        SSH_CONNECTION: _juniper_get_vlan_ssh,
        NETCONF_CONNECTION: _juniper_get_vlan_netconf,
        NAPALM_CONNECTION: _generic_vlan_napalm
    },
    CUMULUS_PLATEFORM_NAME: {
        API_CONNECTION: _cumulus_get_vlan_api,
        SSH_CONNECTION: _cumulus_get_vlan_ssh,
        NETCONF_CONNECTION: _cumulus_get_vlan_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    },
    ARISTA_PLATEFORM_NAME: {
        API_CONNECTION: _arista_get_vlan_api,
        SSH_CONNECTION: _arista_get_vlan_ssh,
        NETCONF_CONNECTION: _arista_get_vlan_netconf,
        NAPALM_CONNECTION: _generic_vlan_napalm
    },
    NEXUS_PLATEFORM_NAME: {
        API_CONNECTION: _nxos_get_vlan_api,
        SSH_CONNECTION: _nxos_get_vlan_ssh,
        NETCONF_CONNECTION: _nxos_get_vlan_netconf,
        NAPALM_CONNECTION: _generic_vlan_napalm
    },
    CISCO_IOS_PLATEFORM_NAME: {
        API_CONNECTION: _ios_get_vlan_api,
        SSH_CONNECTION: _ios_get_vlan_ssh,
        NETCONF_CONNECTION: _ios_get_vlan_netconf,
        NAPALM_CONNECTION: _generic_vlan_napalm
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: _iosxr_get_vlan_api,
        SSH_CONNECTION: _iosxr_get_vlan_ssh,
        NETCONF_CONNECTION: _iosxr_get_vlan_netconf,
        NAPALM_CONNECTION: _generic_vlan_napalm
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: _extreme_vsp_get_vlan_api,
        SSH_CONNECTION: _extreme_vsp_get_vlan_ssh,
        NETCONF_CONNECTION: _extreme_vsp_get_vlan_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    }
}


def get_vlan(nr: Nornir, options={}):

    devices = nr.filter()

    if len(devices.inventory.hosts) == 0:
        raise Exception(f"[{HEADER}] no device selected.")

    if (
        options.get('filters') is not None and 
        options.get('filters').get("get_bond", True)
    ):
        get_bond(
            nr=nr,
            options=options.get('filters')
        )

    data = devices.run(
        task=generic_vlan_get,
        options=options,
        on_failed=True
    )
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL2
    ):
        print_result(data)


def generic_vlan_get(task, options={}):
    base_selection(
        platform=task.host.platform,
        connection_mode=task.host.data.get("connexion"),
        functions_mapping=MAPPING_FUNCTION
    )(task, options)
