#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.protocols.vrf import VRF, ListVRF


def _iosxr_vrf_nc_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if cmd_output.get('VRF') is not None:
        cmd_output['VRF'] = format_xml_output(cmd_output.get('VRF'))
    if cmd_output.get('BGP') is not None:
        cmd_output['BGP'] = format_xml_output(cmd_output.get('BGP'))

    vrf_list = ListVRF(vrf_lst=list())

    vrf_list.vrf_lst.append(
        VRF(
            vrf_name="default",
            vrf_id=NOT_SET,
            vrf_type=NOT_SET,
            l3_vni=NOT_SET,
            rd=NOT_SET,
            rt_imp=NOT_SET,
            rt_exp=NOT_SET,
            imp_targ=NOT_SET,
            exp_targ=NOT_SET,
            options=options
        )
    )

    if (
        'VRF' in cmd_output.keys() and
        'data' in cmd_output.get('VRF').keys() and
        'vrfs' in cmd_output.get('VRF').get('data').keys() and
        'vrf' in cmd_output.get('VRF').get('data').get('vrfs').keys()
    ):
        if isinstance(
            cmd_output.get('VRF').get('data').get('vrfs').get('vrf'),
            dict
        ):
            rias = None
            riin = None
            reas = None
            rein = None
            v = cmd_output.get('VRF').get('data').get('vrfs').get('vrf')
            if (
                    'afs' in v.keys() and
                    'af' in v.get('afs').keys() and
                    'bgp' in v.get('afs').get('af').keys()
            ):
                rias = v.get('afs').get('af').get('bgp') \
                                             .get('import-route-targets') \
                                             .get('route-targets') \
                                             .get('route-target') \
                                             .get('as-or-four-byte-as') \
                                             .get('as')

                riin = v.get('afs').get('af').get('bgp') \
                                             .get('import-route-targets') \
                                             .get('route-targets') \
                                             .get('route-target') \
                                             .get('as-or-four-byte-as') \
                                             .get('as-index')

                reas = v.get('afs').get('af').get('bgp') \
                                             .get('export-route-targets') \
                                             .get('route-targets') \
                                             .get('route-target') \
                                             .get('as-or-four-byte-as') \
                                             .get('as')

                rein = v.get('afs').get('af').get('bgp') \
                                             .get('export-route-targets') \
                                             .get('route-targets') \
                                             .get('route-target') \
                                             .get('as-or-four-byte-as') \
                                             .get('as-index')

            rd = NOT_SET
            if (
                cmd_output.get('BGP') is not None and
                'data' in cmd_output.get('BGP').keys() and
                'bgp' in cmd_output.get('BGP')
                                .get('data').keys() and
                'instance' in cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp').keys() and
                'instance-as' in cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp')
                                        .get('instance').keys() and
                'four-byte-as' in cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp')
                                        .get('instance')
                                        .get('instance-as').keys() and
                'vrfs' in cmd_output.get('BGP')
                                    .get('data')
                                    .get('bgp')
                                    .get('instance')
                                    .get('instance-as')
                                    .get('four-byte-as').keys() and
                'vrf' in cmd_output.get('BGP')
                                    .get('data')
                                    .get('bgp')
                                    .get('instance')
                                    .get('instance-as')
                                    .get('four-byte-as')
                                    .get('vrfs').keys()
            ):
                if isinstance(cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp')
                                        .get('instance')
                                        .get('instance-as')
                                        .get('four-byte-as')
                                        .get('vrfs')
                                        .get('vrf'), dict):
                    vrf = cmd_output.get('BGP') \
                                    .get('data') \
                                    .get('bgp') \
                                    .get('instance') \
                                    .get('instance-as') \
                                    .get('four-byte-as') \
                                    .get('vrfs') \
                                    .get('vrf')
                    if vrf.get('vrf-name') == v.get('vrf-name'):
                        if (
                            'vrf-global' in vrf.keys() and
                            'route-distinguisher' in vrf.get('vrf-global')
                                                            .keys()
                        ):
                            rd = vrf.get('vrf-global') \
                                    .get('route-distinguisher') \
                                    .get('as') + ":" + \
                                vrf.get('vrf-global') \
                                    .get('route-distinguisher') \
                                    .get('as-index')

                elif isinstance(cmd_output.get('BGP')
                                          .get('data')
                                          .get('bgp')
                                          .get('instance')
                                          .get('instance-as')
                                          .get('four-byte-as')
                                          .get('vrfs')
                                          .get('vrf'), list):

                    for vrf in cmd_output.get('BGP') \
                                         .get('data') \
                                         .get('bgp') \
                                         .get('instance') \
                                         .get('instance-as') \
                                         .get('four-byte-as') \
                                         .get('vrfs') \
                                         .get('vrf'):
                        if vrf.get('vrf-name') == v.get('vrf-name'):
                            if (
                                'vrf-global' in vrf.keys() and
                                'route-distinguisher' in
                                vrf.get('vrf-global').keys()
                            ):
                                rd = vrf.get('vrf-global') \
                                        .get('route-distinguisher') \
                                        .get('as') + ":" + \
                                    vrf.get('vrf-global') \
                                        .get('route-distinguisher') \
                                        .get('as-index')
            vrf_list.vrf_lst.append(
                VRF(
                    vrf_name=v.get('vrf-name'),
                    vrf_id=NOT_SET,
                    vrf_type=NOT_SET,
                    l3_vni=NOT_SET,
                    rd=rd,
                    rt_imp=f"{rias}:{riin}" if rias is not None else NOT_SET,
                    rt_exp=f"{reas}:{rein}" if reas is not None else NOT_SET,
                    imp_targ=NOT_SET,
                    exp_targ=NOT_SET,
                    options=options
                )
            )

        elif isinstance(
            cmd_output.get('VRF').get('data').get('vrfs').get('vrf'),
            list
        ):
            for v in cmd_output.get('VRF').get('data').get('vrfs').get('vrf'):
                rias = None
                riin = None
                reas = None
                rein = None
                if (
                    'afs' in v.keys() and 'af' in v.get('afs').keys() and
                    'bgp' in v.get('afs').get('af').keys()
                ):
                    rias = v.get('afs').get('af').get('bgp') \
                                                 .get('import-route-targets') \
                                                 .get('route-targets') \
                                                 .get('route-target') \
                                                 .get('as-or-four-byte-as') \
                                                 .get('as')

                    riin = v.get('afs').get('af').get('bgp') \
                                                 .get('import-route-targets') \
                                                 .get('route-targets') \
                                                 .get('route-target') \
                                                 .get('as-or-four-byte-as') \
                                                 .get('as-index')

                    reas = v.get('afs').get('af').get('bgp') \
                                                 .get('export-route-targets') \
                                                 .get('route-targets') \
                                                 .get('route-target') \
                                                 .get('as-or-four-byte-as') \
                                                 .get('as')

                    rein = v.get('afs').get('af').get('bgp') \
                                                 .get('export-route-targets') \
                                                 .get('route-targets') \
                                                 .get('route-target') \
                                                 .get('as-or-four-byte-as') \
                                                 .get('as-index')

                rd = NOT_SET
                if (
                    cmd_output.get('BGP') is not None and
                    'data' in cmd_output.get('BGP').keys() and
                    'bgp' in cmd_output.get('BGP')
                                    .get('data').keys() and
                    'instance' in cmd_output.get('BGP')
                                            .get('data')
                                            .get('bgp').keys() and
                    'instance-as' in cmd_output.get('BGP')
                                            .get('data')
                                            .get('bgp')
                                            .get('instance').keys() and
                    'four-byte-as' in cmd_output.get('BGP')
                                            .get('data')
                                            .get('bgp')
                                            .get('instance')
                                            .get('instance-as').keys() and
                    'vrfs' in cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp')
                                        .get('instance')
                                        .get('instance-as')
                                        .get('four-byte-as').keys() and
                    'vrf' in cmd_output.get('BGP')
                                        .get('data')
                                        .get('bgp')
                                        .get('instance')
                                        .get('instance-as')
                                        .get('four-byte-as')
                                        .get('vrfs').keys()
                ):
                    if isinstance(cmd_output.get('BGP')
                                            .get('data')
                                            .get('bgp')
                                            .get('instance')
                                            .get('instance-as')
                                            .get('four-byte-as')
                                            .get('vrfs')
                                            .get('vrf'), dict):
                        vrf = cmd_output.get('BGP') \
                                        .get('data') \
                                        .get('bgp') \
                                        .get('instance') \
                                        .get('instance-as') \
                                        .get('four-byte-as') \
                                        .get('vrfs') \
                                        .get('vrf')
                        if vrf.get('vrf-name') == v.get('vrf-name'):
                            if (
                                'vrf-global' in vrf.keys() and
                                'route-distinguisher' in vrf.get('vrf-global')
                                                                .keys()
                            ):
                                rd = vrf.get('vrf-global') \
                                        .get('route-distinguisher') \
                                        .get('as') + ":" + \
                                    vrf.get('vrf-global') \
                                        .get('route-distinguisher') \
                                        .get('as-index')

                    elif isinstance(cmd_output.get('BGP')
                                              .get('data')
                                              .get('bgp')
                                              .get('instance')
                                              .get('instance-as')
                                              .get('four-byte-as')
                                              .get('vrfs')
                                              .get('vrf'), list):

                        for vrf in cmd_output.get('BGP') \
                                             .get('data') \
                                             .get('bgp') \
                                             .get('instance') \
                                             .get('instance-as') \
                                             .get('four-byte-as') \
                                             .get('vrfs') \
                                             .get('vrf'):
                            if vrf.get('vrf-name') == v.get('vrf-name'):
                                if (
                                    'vrf-global' in vrf.keys() and
                                    'route-distinguisher' in
                                    vrf.get('vrf-global').keys()
                                ):
                                    rd = vrf.get('vrf-global') \
                                            .get('route-distinguisher') \
                                            .get('as') + ":" + \
                                        vrf.get('vrf-global') \
                                            .get('route-distinguisher') \
                                            .get('as-index')

                vrf_list.vrf_lst.append(
                    VRF(
                        vrf_name=v.get('vrf-name'),
                        vrf_id=NOT_SET,
                        vrf_type=NOT_SET,
                        l3_vni=NOT_SET,
                        rd=rd,
                        rt_imp=f"{rias}:{riin}"
                                    if rias is not None else NOT_SET,
                        rt_exp=f"{reas}:{rein}"
                                    if reas is not None else NOT_SET,
                        imp_targ=NOT_SET,
                        exp_targ=NOT_SET,
                        options=options
                    )
                )

    return vrf_list
