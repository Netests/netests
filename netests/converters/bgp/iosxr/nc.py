#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.tools.nc import format_xml_output
from netests.constants import NOT_SET
from netests.protocols.bgp import (
    BGPSession,
    ListBGPSessions,
    BGPSessionsVRF,
    ListBGPSessionsVRF,
    BGP
)


def _iosxr_bgp_nc_converter(
    hostname: str,
    cmd_output: dict,
    options={}
) -> BGP:

    bgp_sessions_vrf_lst = ListBGPSessionsVRF(
        list()
    )

    cmd_output = format_xml_output(cmd_output)

    if (
        'data' in cmd_output.keys() and
        'bgp' in cmd_output.get('data').keys() and
        'instance' in cmd_output.get('data').get('bgp').keys() and
        'instance-as' in cmd_output.get('data')
                                   .get('bgp')
                                   .get('instance')
                                   .keys() and
        'four-byte-as' in cmd_output.get('data')
                                    .get('bgp')
                                    .get('instance')
                                    .get('instance-as')
                                    .keys()
    ):
        w = cmd_output.get('data') \
                      .get('bgp') \
                      .get('instance') \
                      .get('instance-as') \
                      .get('four-byte-as')
        as_number = NOT_SET

        # Retrieve information from the Default VRF
        if 'default-vrf' in w.keys():
            bgp_sessions_lst = ListBGPSessions(
                list()
            )
            as_number = w.get('as', NOT_SET)
            # If there is only one BGP neighbors
            if (
                'default-vrf' in w.keys() and
                'bgp-entity' in w.get('default-vrf').keys() and
                isinstance(
                    w.get('default-vrf')
                     .get('bgp-entity')
                     .get('neighbors')
                     .get('neighbor'),
                    dict
                )
            ):
                remote_as = NOT_SET
                if (
                    'remote-as' in
                    w.get('default-vrf')
                     .get('bgp-entity')
                     .get('neighbors')
                     .get('neighbor')
                     .get('neighbor-address')
                     .keys()
                ):
                    remote_as = w.get('default-vrf') \
                                 .get('bgp-entity') \
                                 .get('neighbors') \
                                 .get('neighbor-address') \
                                 .get('remote-as') \
                                 .get('as-yy', NOT_SET)

                bgp_sessions_lst.bgp_sessions.append(
                    BGPSession(
                        src_hostname=hostname,
                        peer_ip=w.get('default-vrf').get(
                            'bgp-entity').get('neighbors').get(
                                'neighbor-address', NOT_SET),
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
                        vrf_name='default',
                        as_number=w.get('as', NOT_SET),
                        router_id=w.get('router-id', NOT_SET),
                        bgp_sessions=bgp_sessions_lst
                    )
                )

            # If there is many BGP neighbors
            elif (
                'default-vrf' in w.keys() and
                'bgp-entity' in w.get('default-vrf').keys() and
                isinstance(
                    w.get('default-vrf')
                     .get('bgp-entity')
                     .get('neighbors')
                     .get('neighbor'),
                    dict
                )
            ):
                for neighbor in w.get('default-vrf') \
                                 .get('bgp-entity') \
                                 .get('neighbors') \
                                 .get('neighbor'):

                    remote_as = NOT_SET
                    if 'remote-as' in neighbor.get('neighbor-address'):
                        remote_as = neighbor.get(
                            'neighbor-address').get(
                            'remote-as').get(
                            'as-yy', NOT_SET),

                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=neighbor.get(
                                'neighbor-address', NOT_SET),
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
                        vrf_name='default',
                        as_number=w.get('as', NOT_SET),
                        router_id=w.get('router-id', NOT_SET),
                        bgp_sessions=bgp_sessions_lst
                    )
                )

        # For different VRF present on the Cisco IOS-XR
        if 'vrfs' in w.keys() and 'vrf' in w.get('vrfs').keys():
            if isinstance(w.get('vrfs').get('vrf'), dict):
                bgp_sessions_lst = ListBGPSessions(
                    list()
                )

                vrf = w.get('vrfs').get('vrf')
                # Only one VRF with Only one BGP neighbor
                if isinstance(
                    vrf.get('vrf-neighbors').get('vrf-neighbor'),
                    dict
                ):
                    remote_as = NOT_SET
                    if (
                        'remote-as' in vrf.get('vrf-neighbors')
                                          .get('vrf-neighbor')
                                          .keys() and
                        'as-yy' in vrf.get('vrf-neighbors')
                                      .get('vrf-neighbor')
                                      .get('remote-as')
                                      .keys()
                    ):
                        remote_as = vrf.get('vrf-neighbors') \
                                       .get('vrf-neighbor') \
                                       .get('remote-as') \
                                       .get('as-yy', NOT_SET)

                    bgp_sessions_lst.bgp_sessions.append(
                        BGPSession(
                            src_hostname=hostname,
                            peer_ip=vrf.get('vrf-neighbors')
                                       .get('vrf-neighbor')
                                       .get('neighbor-address', NOT_SET),
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
                            vrf_name=vrf.get('vrf-name', NOT_SET),
                            as_number=as_number,
                            router_id=vrf.get('vrf-global')
                                         .get('router-id', NOT_SET),
                            bgp_sessions=bgp_sessions_lst
                        )
                    )

                # Only one VRF with multiple BGP neighbors
                elif isinstance(
                    vrf.get('vrf-neighbors').get('vrf-neighbor'),
                    list
                ):
                    for neighbor in vrf.get('vrf-neighbors') \
                                       .get('vrf-neighbor'):

                        remote_as = NOT_SET
                        if 'remote-as' in neighbor.get('remote-as').keys():
                            remote_as = w.get('remote-as').get('as-yy')

                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=neighbor.get(
                                    'neighbor-address', NOT_SET),
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
                            vrf_name='default',
                            as_number=w.get('as', NOT_SET),
                            router_id=w.get('vrf-global')
                                       .get('router-id', NOT_SET),
                            bgp_sessions=bgp_sessions_lst
                        )
                    )

            # Mupltiple VRF
            elif isinstance(w.get('vrfs').get('vrf'), list):
                for vrf in w.get('vrfs').get('vrf'):
                    bgp_sessions_lst = ListBGPSessions(list())
                    # Mupltiple VRF and Only one BGP neighbor in the VRF
                    if isinstance(
                        vrf.get('vrf-neighbors').get('vrf-neighbor'),
                        dict
                    ):
                        remote_as = NOT_SET
                        if (
                            'remote-as' in vrf.get('vrf-neighbors')
                                              .get('vrf-neighbor')
                                              .keys() and
                            'as-yy' in vrf.get('vrf-neighbors')
                                          .get('vrf-neighbor')
                                          .get('remote-as').keys()
                        ):
                            remote_as = vrf.get('vrf-neighbors') \
                                           .get('vrf-neighbor') \
                                           .get('remote-as') \
                                           .get('as-yy', NOT_SET)

                        bgp_sessions_lst.bgp_sessions.append(
                            BGPSession(
                                src_hostname=hostname,
                                peer_ip=vrf.get('vrf-neighbors')
                                           .get('vrf-neighbor')
                                           .get('neighbor-address', NOT_SET),
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
                                vrf_name=vrf.get('vrf-name', NOT_SET),
                                as_number=as_number,
                                router_id=vrf.get('vrf-global')
                                             .get('router-id', NOT_SET),
                                bgp_sessions=bgp_sessions_lst
                            )
                        )

                    # Mupltiple VRF and multiple BGP neighbor in the VRF
                    elif isinstance(
                            vrf.get('vrf-neighbors').get('vrf-neighbor'),
                            list
                    ):
                        for neighbor in vrf.get('vrf-neighbors') \
                                           .get('vrf-neighbor'):

                            remote_as = NOT_SET
                            if 'remote-as' in neighbor.get('remote-as').keys():
                                remote_as = w.get('remote-as').get('as-yy')

                            bgp_sessions_lst.bgp_sessions.append(
                                BGPSession(
                                    src_hostname=hostname,
                                    peer_ip=neighbor.get(
                                        'neighbor-address', NOT_SET),
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
                                vrf_name=vrf.get('vrf-name', NOT_SET),
                                as_number=as_number,
                                router_id=vrf.get('vrf-global')
                                             .get('router-id', NOT_SET),
                                bgp_sessions=bgp_sessions_lst
                            )
                        )

    return BGP(
        hostname=hostname,
        bgp_sessions_vrf_lst=bgp_sessions_vrf_lst
    )
