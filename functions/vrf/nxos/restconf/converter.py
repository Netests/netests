#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.netconf_tools import format_xml_output
from const.constants import NOT_SET, LEVEL1, LEVEL4, LEVEL5
from protocols.vrf import VRF, ListVRF
from functions.verbose_mode import verbose_mode
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _nxos_vrf_restconf_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(type(cmd_output))
        print(cmd_output)

    cmd_output = format_xml_output(cmd_output)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(type(cmd_output))
        PP.pprint(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())

    for v in cmd_output.get('inst-items').get('Inst-list'):

        rd = NOT_SET
        rt_exp = NOT_SET
        rt_imp = NOT_SET
        if (
            'dom-items' in v.keys() and
            'Dom-list' in v.get('dom-items') and
            'af-items' in v.get('dom-items').get('Dom-list').keys() and
            'DomAf-list' in v.get('dom-items')
                             .get('Dom-list')
                             .get('af-items').keys() and
            'ctrl-items' in v.get('dom-items')
                             .get('Dom-list')
                             .get('af-items')
                             .get('DomAf-list').keys() and
            'AfCtrl-list' in v.get('dom-items')
                              .get('Dom-list')
                              .get('af-items')
                              .get('DomAf-list')
                              .get('ctrl-items').keys() and
            'rttp-items' in v.get('dom-items')
                             .get('Dom-list')
                             .get('af-items')
                             .get('DomAf-list')
                             .get('ctrl-items')
                             .get('AfCtrl-list').keys() and
            'RttP-list' in v.get('dom-items')
                            .get('Dom-list')
                            .get('af-items')
                            .get('DomAf-list')
                            .get('ctrl-items')
                            .get('AfCtrl-list')
                            .get('rttp-items').keys()
        ):
            for i in v.get('dom-items') \
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
            'dom-items' in v.keys() and
            'Dom-list' in v.get('dom-items') and
            'rd' in v.get('dom-items').get('Dom-list').keys()
        ):
            t = v.get('dom-items') \
                 .get('Dom-list') \
                 .get('rd').split(':')
            rd = f"{t[-2]}:{t[-1]}"

        vrf_list.vrf_lst.append(
            VRF(
                vrf_name=v.get('name', NOT_SET),
                vrf_id=v.get('id', NOT_SET),
                vrf_type=NOT_SET,
                l3_vni=v.get('encap', NOT_SET),
                rd=rd,
                rt_imp=rt_imp,
                rt_exp=rt_exp,
                imp_targ=NOT_SET,
                exp_targ=NOT_SET,
                options=options
            )
        )

    return vrf_list
