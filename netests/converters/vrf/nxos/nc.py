#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.constants import NOT_SET
from netests.tools.nc import format_xml_output
from netests.protocols.vrf import VRF, ListVRF


def _nxos_vrf_nc_converter(
    hostname: str(),
    cmd_output: list,
    options={}
) -> ListVRF:

    cmd_output = format_xml_output(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())

    for vrf in cmd_output.get('data') \
                         .get('System') \
                         .get('inst-items') \
                         .get('Inst-list'):
        rd = NOT_SET
        rt_exp = NOT_SET
        rt_imp = NOT_SET
        if (
            'dom-items' in vrf.keys() and
            'Dom-list' in vrf.get('dom-items') and
            'af-items' in vrf.get('dom-items').get('Dom-list').keys() and
            'DomAf-list' in vrf.get('dom-items')
                               .get('Dom-list')
                               .get('af-items').keys() and
            'ctrl-items' in vrf.get('dom-items')
                               .get('Dom-list')
                               .get('af-items')
                               .get('DomAf-list').keys() and
            'AfCtrl-list' in vrf.get('dom-items')
                                .get('Dom-list')
                                .get('af-items')
                                .get('DomAf-list')
                                .get('ctrl-items').keys() and
            'rttp-items' in vrf.get('dom-items')
                               .get('Dom-list')
                               .get('af-items')
                               .get('DomAf-list')
                               .get('ctrl-items')
                               .get('AfCtrl-list').keys() and
            'RttP-list' in vrf.get('dom-items')
                              .get('Dom-list')
                              .get('af-items')
                              .get('DomAf-list')
                              .get('ctrl-items')
                              .get('AfCtrl-list')
                              .get('rttp-items').keys()
        ):
            for i in vrf.get('dom-items') \
                        .get('Dom-list') \
                        .get('af-items') \
                        .get('DomAf-list') \
                        .get('ctrl-items') \
                        .get('AfCtrl-list') \
                        .get('rttp-items') \
                        .get('RttP-list'):

                if i.get('type', NOT_SET) == 'export':
                    if (
                        'ent-items' in i.keys() and
                        'RttEntry-list' in i.get('ent-items').keys() and
                        'rtt' in i.get('ent-items').get('RttEntry-list').keys()
                    ):
                        y = i.get('ent-items') \
                             .get('RttEntry-list') \
                             .get('rtt').split(':')
                        rt_exp = f"{y[-2]}:{y[-1]}"

                if i.get('type', NOT_SET) == 'import':
                    if (
                        'ent-items' in i.keys() and
                        'RttEntry-list' in i.get('ent-items').keys() and
                        'rtt' in i.get('ent-items').get('RttEntry-list').keys()
                    ):
                        z = i.get('ent-items') \
                             .get('RttEntry-list') \
                             .get('rtt').split(':')
                        rt_imp = f"{z[-2]}:{z[-1]}"

        if (
            'dom-items' in vrf.keys() and
            'Dom-list' in vrf.get('dom-items') and
            'rd' in vrf.get('dom-items').get('Dom-list').keys()
        ):
            t = vrf.get('dom-items') \
                   .get('Dom-list') \
                   .get('rd').split(':')
            rd = f"{t[-2]}:{t[-1]}"

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=vrf.get('name', NOT_SET),
                vrf_id=NOT_SET,
                vrf_type=NOT_SET,
                l3_vni=vrf.get('encap', NOT_SET),
                rd=rd,
                rt_imp=rt_imp,
                rt_exp=rt_exp,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET,
                options=options
            )
        )

    return vrf_list
