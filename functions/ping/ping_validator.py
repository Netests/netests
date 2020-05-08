#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from exceptions.netests_exceptions import NetestsErrorWithPingExecution


HEADER = "[netests - _raise_exception_on_ping_cmd]"


def _raise_exception_on_ping_cmd(
    output: str,
    hostname: str,
    ping_line: str,
    must_work: bool
) -> None:

    if must_work:
        if (
            (
                # For Cisco NXOS
                "address is not permitted" in output or
                "No route to host" in output or
                "100.00% packet loss" in output or
                "0 packets received" in output or
                "ping: bad context" in output or
                "Invalid host/interface" in output
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
        print(output)
        # PING MUST NOT WORK !
        # Defined that a ping is working to raise an Error
        if (
            (
                # For Juniper VMX
                "1 packets received" in output and
                "0% packet loss" in output
            ) or
            (
                # For Cisco NXOS
                "1 packets received" in output or
                # DONT REMOVE THE SPACE BEFORE THE '0' !!!
                " 0.00% packet loss" in output
            ) or
            (
                "1 received" in output and
                "0% packet loss" in output
            ) or
            (
                # For Extreme Networks
                "is alive" in output
            ) or
            "Success rate is 100 percent" in output
        ):
            raise NetestsErrorWithPingExecution(
                f"{HEADER}({hostname}) the following ping raise an error "
                f"{ping_line}"
            )
