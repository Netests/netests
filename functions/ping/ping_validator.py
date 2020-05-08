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
    NEXUS_PLATEFORM_NAME
)


HEADER = "[netests - _raise_exception_on_ping_cmd]"


def _raise_exception_on_ping_cmd(
    output: str,
    hostname: str,
    platform: str,
    ping_line: str,
    must_work: bool
) -> None:

    if must_work:
        if (
            (
                # For Arista Networks
                platform == ARISTA_PLATEFORM_NAME and
                (
                    "Network is unreachable" in output or
                    "Temporary failure in name resolution" in output or
                    "100% packet loss" in output or
                    "0 received" in output or
                    "Invalid input - VRF" in output
                )
            ) or
            (
                # For Cisco NXOS
                platform == NEXUS_PLATEFORM_NAME and
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
                (
                    "Bad hostname or protocol" in output or
                    "Success rate is 0 percent" in output or
                    "Invalid vrf table name" in output
                )
            )or
            (
                # For Cisco IOS-XE
                platform == CISCO_IOS_PLATEFORM_NAME and
                (
                    "Unrecognized host or address" in output or
                    "Success rate is 0 percent" in output or
                    "Invalid input detected at" in output
                )
            ) or
            (
                # For Extreme Networks
                platform == EXTREME_PLATEFORM_NAME and
                (
                    "The VRF Name entered does not correspond" in output or
                    "no answer from" in output or
                    "Invalid host name format or IP address" in output
                )
            ) or
            "Invalid host/interface " in output or
            "Network is unreachable" in output or
            "Temporary failure in name resolution" in output or
            "100% packet loss" in output or
            "0 received" in output or
            "Success rate is 0 percent" in output or
            "invalid routing instance" in output or
            "no answer from" in output or
            "ping: timeout" in output
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
                    "rtt min/avg/max/mdev" in output or
                    "1 packets transmitted" in output or
                    "1 received" in output or
                    "0% packet loss" in output
                )
            ) or
            (
                # For Juniper VMX
                platform == JUNOS_PLATEFORM_NAME and
                (
                    "1 packets received" in output or
                    "0% packet loss" in output
                )
            ) or
            (
                # For Cisco NXOS
                platform == NEXUS_PLATEFORM_NAME and
                (
                    "1 packets received" in output or
                    # DONT REMOVE THE SPACE BEFORE THE '0' !!!
                    " 0.00% packet loss" in output
                )
            ) or
            (
                # For Cisco IOS-XR
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                (
                    "Success rate is 100 percent" in output or
                    "round-trip min/avg/max" in output
                )
            ) or
            (
                # For Cisco IOS-XE
                platform == CISCO_IOSXR_PLATEFORM_NAME and
                (
                    "Success rate is 100 percent" in output or
                    "round-trip min/avg/max" in output
                )
            ) or
            (
                # For Cumulus
                platform == CUMULUS_PLATEFORM_NAME and
                (
                    "1 received" in output and
                    "0% packet loss" in output
                )
            ) or
            (
                # For Extreme Networks
                platform == EXTREME_PLATEFORM_NAME and
                (
                    "is alive" in output
                )
            ) or
            "Success rate is 100 percent" in output
        ):
            raise NetestsErrorWithPingExecution(
                f"{HEADER}({hostname}) the following ping raise an error "
                f"{ping_line}"
            )
