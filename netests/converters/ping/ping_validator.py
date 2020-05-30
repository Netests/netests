#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.converters.ping.arista.validator import (
    arista_api_ping_validator,
    arista_netconf_ping_validator,
    arista_ssh_ping_validator,
)
from netests.converters.ping.extreme_vsp.validator import (
    extreme_vsp_api_ping_validator,
    extreme_vsp_netconf_ping_validator,
    extreme_vsp_ssh_ping_validator
)
from netests.converters.ping.cumulus.validator import (
    cumulus_api_ping_validator,
    cumulus_netconf_ping_validator,
    cumulus_ssh_ping_validator
)
from netests.converters.ping.ios.validator import (
    ios_api_ping_validator,
    ios_netconf_ping_validator,
    ios_ssh_ping_validator
)
from netests.converters.ping.iosxr.validator import (
    iosxr_api_ping_validator,
    iosxr_netconf_ping_validator,
    iosxr_ssh_ping_validator
)
from netests.converters.ping.juniper.validator import (
    juniper_api_ping_validator,
    juniper_netconf_ping_validator,
    juniper_ssh_ping_validator
)
from netests.converters.ping.nxos.validator import (
    nxos_api_ping_validator,
    nxos_netconf_ping_validator,
    nxos_ssh_ping_validator
)
from netests.constants import (
    ARISTA_PLATEFORM_NAME,
    CUMULUS_PLATEFORM_NAME,
    EXTREME_PLATEFORM_NAME,
    CISCO_IOS_PLATEFORM_NAME,
    CISCO_IOSXR_PLATEFORM_NAME,
    JUNOS_PLATEFORM_NAME,
    NEXUS_PLATEFORM_NAME,
    API_CONNECTION,
    NETCONF_CONNECTION,
    SSH_CONNECTION
)


HEADER = "[netests - _raise_exception_on_ping_cmd]"
M = {
    ARISTA_PLATEFORM_NAME: {
        API_CONNECTION: arista_api_ping_validator,
        NETCONF_CONNECTION: arista_netconf_ping_validator,
        SSH_CONNECTION: arista_ssh_ping_validator
    },
    CUMULUS_PLATEFORM_NAME: {
        API_CONNECTION: cumulus_api_ping_validator,
        NETCONF_CONNECTION: cumulus_netconf_ping_validator,
        SSH_CONNECTION: cumulus_ssh_ping_validator
    },
    EXTREME_PLATEFORM_NAME: {
        API_CONNECTION: extreme_vsp_api_ping_validator,
        NETCONF_CONNECTION: extreme_vsp_netconf_ping_validator,
        SSH_CONNECTION: extreme_vsp_ssh_ping_validator
    },
    CISCO_IOS_PLATEFORM_NAME: {
        API_CONNECTION: ios_api_ping_validator,
        NETCONF_CONNECTION: ios_netconf_ping_validator,
        SSH_CONNECTION: ios_ssh_ping_validator
    },
    CISCO_IOSXR_PLATEFORM_NAME: {
        API_CONNECTION: iosxr_api_ping_validator,
        NETCONF_CONNECTION: iosxr_netconf_ping_validator,
        SSH_CONNECTION: iosxr_ssh_ping_validator
    },
    JUNOS_PLATEFORM_NAME: {
        API_CONNECTION: juniper_api_ping_validator,
        NETCONF_CONNECTION: juniper_netconf_ping_validator,
        SSH_CONNECTION: juniper_ssh_ping_validator
    },
    NEXUS_PLATEFORM_NAME: {
        API_CONNECTION: nxos_api_ping_validator,
        NETCONF_CONNECTION: nxos_netconf_ping_validator,
        SSH_CONNECTION: nxos_ssh_ping_validator
    },
}


def _raise_exception_on_ping_cmd(
    output: str,
    hostname: str,
    platform: str,
    connexion: str,
    ping_line: str,
    must_work: bool
) -> None:
    return M.get(platform).get(connexion)(output, must_work)
