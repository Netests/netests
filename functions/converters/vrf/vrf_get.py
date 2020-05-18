#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from nornir.core import Nornir
from nornir.core.filter import F
from nornir.plugins.functions.text import print_result
from functions.vrf.arista.vrf_arista import (
    _arista_get_vrf_api,
    _arista_get_vrf_netconf,
    _arista_get_vrf_ssh
)
from functions.vrf.cumulus.vrf_cumulus import (
    _cumulus_get_vrf_api,
    _cumulus_get_vrf_netconf,
    _cumulus_get_vrf_ssh
)
from functions.vrf.extreme_vsp.vrf_extreme_vsp import (
    _extreme_vsp_get_vrf_api,
    _extreme_vsp_get_vrf_netconf,
    _extreme_vsp_get_vrf_ssh
)
from functions.vrf.ios.vrf_ios import (
    _ios_get_vrf_api,
    _ios_get_vrf_netconf,
    _ios_get_vrf_ssh
)
from functions.vrf.iosxr.vrf_iosxr import (
    _iosxr_get_vrf_api,
    _iosxr_get_vrf_netconf,
    _iosxr_get_vrf_ssh
)
from functions.vrf.juniper.vrf_juniper import (
    _juniper_get_vrf_api,
    _juniper_get_vrf_netconf,
    _juniper_get_vrf_ssh
)
from functions.vrf.napalm.vrf_napalm import (
    _generic_vrf_napalm
)
from functions.vrf.nxos.vrf_nxos import (
    _nxos_get_vrf_api,
    _nxos_get_vrf_netconf,
    _nxos_get_vrf_ssh
)
from const.constants import (
    NOT_SET,
    LEVEL1,
    LEVEL2,
    VRF_DATA_KEY,
    VRF_NAME_DATA_KEY,
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
import pprint
PP = pprint.PrettyPrinter(indent=4)


HEADER = "[netests - get_vrf]"


MAPPING_FUNCTION = {
    JUNOS_PLATEFORM_NAME: {
        API_CONNECTION: _juniper_get_vrf_api,
        SSH_CONNECTION: _juniper_get_vrf_ssh,
        NETCONF_CONNECTION: _juniper_get_vrf_netconf,
        NAPALM_CONNECTION: _generic_vrf_napalm
    },
    CUMULUS_PLATEFORM_NAME: {
        API_CONNECTION: _cumulus_get_vrf_api,
        SSH_CONNECTION: _cumulus_get_vrf_ssh,
        NETCONF_CONNECTION: _cumulus_get_vrf_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    },
    ARISTA_PLATEFORM_NAME: {
        API_CONNECTION: _arista_get_vrf_api,
        SSH_CONNECTION: _arista_get_vrf_ssh,
        NETCONF_CONNECTION: _arista_get_vrf_netconf,
        NAPALM_CONNECTION: _generic_vrf_napalm
    },
    NEXUS_PLATEFORM_NAME: {
        API_CONNECTION: _nxos_get_vrf_api,
        SSH_CONNECTION: _nxos_get_vrf_ssh,
        NETCONF_CONNECTION: _nxos_get_vrf_netconf,
        NAPALM_CONNECTION: _generic_vrf_napalm
    },
    CISCO_IOS_PLATEFORM_NAME: {
        API_CONNECTION: _ios_get_vrf_api,
        SSH_CONNECTION: _ios_get_vrf_ssh,
        NETCONF_CONNECTION: _ios_get_vrf_netconf,
        NAPALM_CONNECTION: _generic_vrf_napalm
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: _iosxr_get_vrf_api,
        SSH_CONNECTION: _iosxr_get_vrf_ssh,
        NETCONF_CONNECTION: _iosxr_get_vrf_netconf,
        NAPALM_CONNECTION: _generic_vrf_napalm
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: _extreme_vsp_get_vrf_api,
        SSH_CONNECTION: _extreme_vsp_get_vrf_ssh,
        NETCONF_CONNECTION: _extreme_vsp_get_vrf_netconf,
        NAPALM_CONNECTION: device_not_compatible_with_napalm
    }
}


def get_vrf(nr: Nornir, options={}):
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

    else:
        data = devices.run(
            task=generic_vrf_get,
            on_failed=True,
            options=options
        )

        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL2
        ):
            for host in devices.inventory.hosts:
                if VRF_DATA_KEY in devices.inventory.hosts.get(host).keys():
                    PP.pprint(
                        devices.inventory.hosts.get(host)
                                               .get(VRF_DATA_KEY)
                                               .to_json()
                    )

        data = devices.run(
            task=save_vrf_name_in_a_list,
            on_failed=True,
            num_workers=10
        )
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL2
        ):
            print_result(data)


def generic_vrf_get(task, options={}):
    base_selection(
        platform=task.host.platform,
        connection_mode=task.host.data.get("connexion"),
        functions_mapping=MAPPING_FUNCTION
    )(task, options)


def save_vrf_name_in_a_list(task):
    vrf_name_lst = dict()

    for vrf in task.host[VRF_DATA_KEY].vrf_lst:
        vrf_name_lst[vrf.vrf_name] = vrf.vrf_id

    task.host[VRF_NAME_DATA_KEY] = vrf_name_lst
