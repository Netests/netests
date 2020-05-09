#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsErrorWithPingExecution
from const.constants import (
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


def _raise_exception_on_ping_cmd(
    output: str,
    hostname: str,
    platform: str,
    connexion: str,
    ping_line: str,
    must_work: bool
) -> None:
    if must_work:
        if (
            (
                # For Arista Networks
                platform == ARISTA_PLATEFORM_NAME and
                (
                    connexion == SSH_CONNECTION or
                    connexion == API_CONNECTION
                ) and
                (
                    "Network is unreachable" in output or
                    "failure in name resolution" in output or
                    "100% packet loss" in output or
                    "0 received" in output or
                    "Invalid input - VRF" in output
                )
            ) or
            (
                # For Cisco NXOS
                platform == NEXUS_PLATEFORM_NAME and
                (
                    connexion == SSH_CONNECTION or
                    connexion == API_CONNECTION
                ) and
                (
                    "address is not permitted" in output or
                    "No route to host" in output or
                    "100.00% packet loss" in output or
                    "0 packets received" in output or
                    "ping: bad context" in output or
                    "Invalid host/interface" in output
                )
            ) or
            (
                # For Cisco IOS-XR
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "Bad hostname or protocol" in output or
                    "Success rate is 0 percent" in output or
                    "Invalid vrf table name" in output
                )
            )or
            (
                # For Cisco IOS-XR NETCONF
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                connexion == NETCONF_CONNECTION and
                validate_iosxr_do_we_raise_error(output, True)
            ) or
            (
                # For Cisco IOS-XE
                platform == CISCO_IOS_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "Unrecognized host or address" in output or
                    "Success rate is 0 percent" in output or
                    "Invalid input detected at" in output or
                    "Unable to find vrf" in output or
                    "does not have a usable source address" in output
                )
            ) or
            (
                # For Extreme Networks
                platform == EXTREME_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "The VRF Name entered does not correspond" in output or
                    "no answer from" in output or
                    "Invalid host name format or IP address" in output
                )
            )
        ):
            raise NetestsErrorWithPingExecution(
                f"{HEADER}({hostname}) the following ping raise an error "
                f"{ping_line}"
            )
    else:
        # PING MUST NOT WORK !
        # Defined that a ping is working to raise an Error
        if (
            (
                # For Arista Networks
                platform == ARISTA_PLATEFORM_NAME and
                (
                    connexion == SSH_CONNECTION or
                    connexion == API_CONNECTION
                ) and 
                (
                    "rtt min/avg/max/mdev" in output or
                    "1 received" in output or
                    # DONT REMOVE THE SPACE BEFORE THE '0' !!!
                    " 0% packet loss" in output
                )
            ) or
            (
                # For Juniper VMX
                platform == JUNOS_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "1 packets received" in output or
                    "0% packet loss" in output
                )
            ) or
            (
                # For Cisco NXOS
                platform == NEXUS_PLATEFORM_NAME and
                (
                    connexion == SSH_CONNECTION or
                    connexion == NETCONF_CONNECTION
                ) and
                (
                    "1 packets received" in output or
                    # DONT REMOVE THE SPACE BEFORE THE '0' !!!
                    " 0.00% packet loss" in output
                )
            ) or
            (
                # For Cisco IOS-XR
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "Success rate is 100 percent" in output or
                    "round-trip min/avg/max" in output
                )
            ) or
            (
                # For Cisco IOS-XR NETCONF
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                connexion == NETCONF_CONNECTION and
                validate_iosxr_do_we_raise_error(output, False)
            ) or 
            (
                # For Cisco IOS-XE
                platform == CISCO_IOS_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "Success rate is 100 percent" in output or
                    "round-trip min/avg/max" in output
                )
            ) or
            (
                # For Cumulus
                platform == CUMULUS_PLATEFORM_NAME and
                connexion == NETCONF_CONNECTION and
                (
                    "1 received" in output and
                    "0% packet loss" in output
                )
            ) or
            (
                # For Extreme Networks
                platform == EXTREME_PLATEFORM_NAME and
                connexion == SSH_CONNECTION and
                (
                    "is alive" in output
                )
            )
        ):
            raise NetestsErrorWithPingExecution(
                f"{HEADER}({hostname}) the following ping raise an error "
                f"{ping_line}"
            )


def validate_iosxr_do_we_raise_error(o, works):
    if (
        isinstance(o, dict) and
        'rpc-reply' in o.keys() and
        'ping-response' in o.get('rpc-reply').keys() and
        'ipv4' in o.get('rpc-reply').get('ping-response').keys()
    ):
        if (
            (
                o.get('rpc-reply')
                 .get('ping-response')
                 .get('ipv4')
                 .get('success-rate') == '100' and
                works is False
            ) or
            (
                o.get('rpc-reply')
                 .get('ping-response')
                 .get('ipv4')
                 .get('success-rate') == '0' and
                works is True
            )
        ):
            return True

    if (
        isinstance(o, dict) and
        'rpc-reply' in o.keys() and
        'rpc-error' in o.get('rpc-reply').keys() and
        works is True
    ):
        return True

    return False
