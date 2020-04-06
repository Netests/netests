#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
from const.constants import (
    NOT_SET
)
from exceptions.netests_iosxr_exceptions import (
    NetestsIOSXRNetconfOutputError
)
from protocols.bgp import (
    LEVEL2,
    LEVEL4,
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)
from functions.global_tools import (
    printline
)
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _iosxr_bgp_netconf_converter(hostname: str, cmd_outputs: dict) -> BGP:
    cmd_outputs = json.loads(cmd_outputs)
    bgp_sessions_vrf_lst = ListBGPSessionsVRF(list())

    if verbose_mode(
        user_value=os.environ["NETESTS_VERBOSE"],
        needed_value=LEVEL4
    ):
        printline()
        PP.pprint(cmd_outputs)

    if (
        "data" in cmd_outputs.keys() and
        "bgp" in cmd_outputs.get("data").keys() and
        "instance" in cmd_outputs.get("data").get("bgp").keys() and
        "instance-as" in cmd_outputs.get("data").get(
            "bgp").get("instance").keys() and
        "four-byte-as" in cmd_outputs.get("data").get(
            "bgp").get("instance").get("instance-as").keys()
    ):
        w = cmd_outputs.get("data") .get("bgp").get("instance").get(
            "instance-as").get("four-byte-as")

        if verbose_mode(
            user_value=os.environ["NETESTS_VERBOSE"],
            needed_value=LEVEL4
        ):
            printline()
            PP.pprint(w)

        as_number = 0

        # Retrieve information from the Default VRF
        if "default-vrf" in w.keys():
            bgp_sessions_lst = ListBGPSessions(list())
            as_number = w.get("as", NOT_SET)
            # If there is only one BGP neighbors
            if isinstance(
                w.get("default-vrf").get("bgp-entity").get(
                    "neighbors").get("neighbor"),
                dict
            ):
                remote_as = NOT_SET
                if (
                    "remote-as" in
                    w.get("default-vrf").get("bgp-entity").get(
                        "neighbors").get("neighbor").get(
                        "neighbor-address").keys()
                ):
                    remote_as = w.get("default-vrf").get("bgp-entity").get(
                        "neighbors").get("neighbor-address").get(
                            "remote-as").get("as-yy", NOT_SET),

                bgp_sessions_lst.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=w.get("default-vrf").get(
                            "bgp-entity").get("neighbors").get(
                                "neighbor-address", NOT_SET),
                        remote_as=remote_as,
                        state_brief=NOT_SET,
                        peer_hostname=NOT_SET,
                        session_state=NOT_SET,
                        state_time=NOT_SET,
                        prefix_received=NOT_SET
                    )
                )

                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                    BGPSessionsVRF(
                        vrf_name="default",
                        as_number=w.get("as", NOT_SET),
                        router_id=w.get("router-id", NOT_SET),
                        bgp_sessions=bgp_sessions_lst
                    )
                )

            # If there is many BGP neighbors
            elif isinstance(
                w.get("default-vrf").get("bgp-entity").get(
                    "neighbors").get("neighbor"),
                list
            ):
                for neighbor in w.get(
                                      "default-vrf").get(
                                      "bgp-entity").get(
                                      "neighbors").get(
                                      "neighbor"):

                    remote_as = NOT_SET
                    if "remote-as" in neighbor.get("neighbor-address"):
                        remote_as = neighbor.get(
                            "neighbor-address").get(
                            "remote-as").get(
                            "as-yy", NOT_SET),

                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=neighbor.get(
                                "neighbor-address", NOT_SET),
                            remote_as=remote_as,
                            state_brief=NOT_SET,
                            peer_hostname=NOT_SET,
                            session_state=NOT_SET,
                            state_time=NOT_SET,
                            prefix_received=NOT_SET
                        )
                    )

                bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                    BGPSessionsVRF(
                        vrf_name="default",
                        as_number=w.get("as", NOT_SET),
                        router_id=w.get("router-id", NOT_SET),
                        bgp_sessions=bgp_sessions_lst
                    )
                )

        # For different VRF present on the Cisco IOS-XR
        if "vrfs" in w.keys() and "vrf" in w.get("vrfs").keys():
            if isinstance(w.get("vrfs").get("vrf"), dict):

                bgp_sessions_lst = ListBGPSessions(list())
                vrf = w.get("vrfs").get("vrf")

                # Only one VRF with Only one BGP neighbor
                if isinstance(
                    vrf.get("vrf-neighbors").get("vrf-neighbors"),
                    dict
                ):
                    remote_as = NOT_SET
                    if (
                        "remote-as" in vrf.get("vrf-neighbors").get(
                            "vrf-neighbor").keys() and
                        "as-yy" in vrf.get("vrf-neighbors").get(
                            "vrf-neighbor").get("remote-as").keys()
                    ):
                        remote_as = vrf.get("vrf-neighbors").get(
                            "remote-as").keys()

                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=vrf.get("vrf-neighbors").get(
                                "vrf-neighbor").get(
                                "neighbor-address", NOT_SET),
                            remote_as=remote_as,
                            state_brief=NOT_SET,
                            peer_hostname=NOT_SET,
                            session_state=NOT_SET,
                            state_time=NOT_SET,
                            prefix_received=NOT_SET
                        )
                    )

                    bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                        BGPSessionsVRF(
                            vrf_name=vrf.get("vrf-name", NOT_SET),
                            as_number=as_number,
                            router_id=w.get("gloabl").get(
                                "router-id", NOT_SET),
                            bgp_sessions=bgp_sessions_lst
                        )
                    )

                # Only one VRF with multiple BGP neighbors
                elif isinstance(
                                vrf.get("vrf-neighbors").get("vrf-neighbor"),
                                list
                ):
                    for neighbor in vrf.get(
                                            "vrf-neighbors").get(
                                            "vrf-neighbors"):

                        remote_as = NOT_SET
                        if ("remote-as" in neighbor.get("remote-as").keys()):
                            remote_as = w.get("remote-as").get("as-yy")

                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=neighbor.get(
                                    "neighbor-address", NOT_SET),
                                remote_as=remote_as,
                                state_brief=NOT_SET,
                                peer_hostname=NOT_SET,
                                session_state=NOT_SET,
                                state_time=NOT_SET,
                                prefix_received=NOT_SET
                            )
                        )

                    bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                        BGPSessionsVRF(
                            vrf_name="default",
                            as_number=w.get("as", NOT_SET),
                            router_id=w.get(
                                            "vrf-gloabl").get(
                                            "router-id", NOT_SET),
                            bgp_sessions=bgp_sessions_lst
                        )
                    )

            # Mupltiple VRF
            elif isinstance(w.get("vrfs").get("vrf"), list):
                for vrf in w.get("vrfs").get("vrf"):
                    bgp_sessions_lst = ListBGPSessions(list())
                    # Mupltiple VRF and Only one BGP neighbor in the VRF
                    if isinstance(
                        vrf.get("vrf-neighbors").get("vrf-neighbor"),
                        dict
                    ):
                        remote_as = NOT_SET
                        if (
                            "remote-as" in vrf.get("vrf-neighbors").get(
                               "vrf-neighbor").keys() and
                            "as-yy" in vrf.get("vrf-neighbors").get(
                             "vrf-neighbor").get("remote-as").keys()
                        ):
                            remote_as = vrf.get(
                                                "vrf-neighbors").get(
                                                "vrf-neighbor").get(
                                                "remote-as").get(
                                                "as-yy", NOT_SET)

                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=vrf.get("vrf-neighbors").get(
                                    "vrf-neighbor").get(
                                    "neighbor-address", NOT_SET),
                                remote_as=remote_as,
                                state_brief=NOT_SET,
                                peer_hostname=NOT_SET,
                                session_state=NOT_SET,
                                state_time=NOT_SET,
                                prefix_received=NOT_SET
                            )
                        )

                        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                            BGPSessionsVRF(
                                vrf_name=vrf.get("vrf-name", NOT_SET),
                                as_number=as_number,
                                router_id=vrf.get("vrf-global").get(
                                    "router-id", NOT_SET),
                                bgp_sessions=bgp_sessions_lst
                            )
                        )

                    # Mupltiple VRF and multiple BGP neighbor in the VRF
                    elif isinstance(
                            vrf.get("vrf-neighbors").get("vrf-neighbor"),
                            list
                    ):
                        for neighbor in vrf.get(
                                                "vrf-neighbors").get(
                                                "vrf-neighbor"):

                            remote_as = NOT_SET
                            if "remote-as" in neighbor.get("remote-as").keys():
                                remote_as = w.get("remote-as").get("as-yy")

                            bgp_sessions_lst.bgp_sessions.append(
                                BGPSession(
                                    src_hostname=hostname,
                                    peer_ip=neighbor.get(
                                        "neighbor-address", NOT_SET),
                                    remote_as=remote_as,
                                    state_brief=NOT_SET,
                                    peer_hostname=NOT_SET,
                                    session_state=NOT_SET,
                                    state_time=NOT_SET,
                                    prefix_received=NOT_SET
                                )
                            )

                        bgp_sessions_vrf_lst.bgp_sessions_vrf.append(
                            BGPSessionsVRF(
                                vrf_name=vrf.get("vrf-name", NOT_SET),
                                as_number=as_number,
                                router_id=vrf.get("vrf-global").get(
                                    "router-id", NOT_SET),
                                bgp_sessions=bgp_sessions_lst
                            )
                        )

    else:
        raise NetestsIOSXRNetconfOutputError(
            f"Netconf call output does not have all keys for device {hostname}"
        )

    bgp = BGP(hostname=hostname, bgp_sessions_vrf_lst=bgp_sessions_vrf_lst)

    if verbose_mode(
        user_value=os.environ["NETESTS_VERBOSE"],
        needed_value=LEVEL2
    ):
        print(bgp)

    return bgp
