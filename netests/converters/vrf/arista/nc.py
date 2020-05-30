#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF
from netests.tools.nc import format_xml_output


def _arista_vrf_nc_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    cmd_output = format_xml_output(cmd_output)

    vrf_list = ListVRF(list())

    if (
        'data' in cmd_output.keys() and
        'network-instances' in cmd_output.get('data').keys() and
        'network-instance' in cmd_output.get('data')
                                        .get('network-instances')
                                        .keys()
    ):

        if isinstance(
            cmd_output.get('data')
                      .get('network-instances')
                      .get('network-instance'),
            dict
        ):

            vrf_list.vrf_lst.append(
                VRF(
                    vrf_name=cmd_output.get('data')
                                       .get('network-instances')
                                       .get('network-instance')
                                       .get('name', NOT_SET),
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

        elif isinstance(
            cmd_output.get('data')
                      .get('network-instances')
                      .get('network-instance'),
            list
        ):
            for v in cmd_output.get('data') \
                               .get('network-instances') \
                               .get('network-instance'):
                vrf_list.vrf_lst.append(
                    VRF(
                        vrf_name=v.get('name', NOT_SET),
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

    return vrf_list
