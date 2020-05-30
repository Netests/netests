#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from netests.constants import NOT_SET
from netests.protocols.vrf import VRF, ListVRF


def _nxos_vrf_api_converter(
    hostname: str(),
    cmd_output,
    options={}
) -> ListVRF:

    if not isinstance(cmd_output, dict):
        cmd_output = json.loads(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())

    if (
        'ins_api' in cmd_output.keys() and
        'outputs' in cmd_output.get('ins_api') and
        'output' in cmd_output.get('ins_api').get('outputs').keys() and
        'body' in cmd_output.get('ins_api')
                            .get('outputs')
                            .get('output').keys() and
        'TABLE_vrf' in cmd_output.get('ins_api')
                                 .get('outputs')
                                 .get('output')
                                 .get('body').keys() and
        'ROW_vrf' in cmd_output.get('ins_api')
                               .get('outputs')
                               .get('output')
                               .get('body')
                               .get('TABLE_vrf').keys()
    ):
        if isinstance(
            cmd_output.get('ins_api')
                      .get('outputs')
                      .get('output')
                      .get('body')
                      .get('TABLE_vrf')
                      .get('ROW_vrf'),
            dict
        ):
            vrf_list.vrf_lst.append(
                VRF(
                    vrf_name=cmd_output.get('ins_api')
                                       .get('outputs')
                                       .get('output')
                                       .get('body')
                                       .get('TABLE_vrf')
                                       .get('ROW_vrf')
                                       .get('vrf_name', NOT_SET),
                    vrf_id=cmd_output.get('ins_api')
                                     .get('outputs')
                                     .get('output')
                                     .get('body')
                                     .get('TABLE_vrf')
                                     .get('ROW_vrf')
                                     .get('vrf_id', NOT_SET),
                    vrf_type=NOT_SET,
                    l3_vni=cmd_output.get('ins_api')
                                     .get('outputs')
                                     .get('output')
                                     .get('body')
                                     .get('TABLE_vrf')
                                     .get('ROW_vrf')
                                     .get('encap', NOT_SET),
                    rd=cmd_output.get('ins_api')
                                 .get('outputs')
                                 .get('output')
                                 .get('body')
                                 .get('TABLE_vrf')
                                 .get('ROW_vrf')
                                 .get('rd', NOT_SET),
                    rt_imp=NOT_SET,
                    rt_exp=NOT_SET,
                    imp_targ=NOT_SET,
                    exp_targ=NOT_SET,
                    options=options
                )
            )

        elif isinstance(
            cmd_output.get('ins_api')
                      .get('outputs')
                      .get('output')
                      .get('body')
                      .get('TABLE_vrf')
                      .get('ROW_vrf'),
            list
        ):
            for v in cmd_output.get('ins_api') \
                               .get('outputs') \
                               .get('output') \
                               .get('body') \
                               .get('TABLE_vrf') \
                               .get('ROW_vrf'):
                vrf_list.vrf_lst.append(
                    VRF(
                        vrf_name=v.get('vrf_name', NOT_SET),
                        vrf_id=v.get('vrf_id', NOT_SET),
                        vrf_type=NOT_SET,
                        l3_vni=v.get('encap', NOT_SET),
                        rd=v.get('rd', NOT_SET),
                        rt_imp=NOT_SET,
                        rt_exp=NOT_SET,
                        imp_targ=NOT_SET,
                        exp_targ=NOT_SET,
                        options=options
                    )
                )

    return vrf_list
